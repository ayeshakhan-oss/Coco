/**
 * Insert Confirmed Candidate to Markaz
 * Run after Ayesha confirms a sourced candidate is interested
 *
 * Usage:
 *   node insert-confirmed-candidate.js --name "Alice Smith" --url "https://linkedin.com/in/alice" ...
 */

const { Client } = require('pg');
require('dotenv').config();

const MARKAZ_WRITE_URL = process.env.MARKAZ_WRITE_URL || 'postgresql://...';

async function insertConfirmedCandidate(candidate, jobId) {
  const client = new Client({ connectionString: MARKAZ_WRITE_URL });

  try {
    await client.connect();
    console.log('Connected to Markaz');

    // Step 1: Check for duplicate by email (skip if email is null for LinkedIn sourced)
    let candidateId;
    if (candidate.email) {
      const existing = await client.query(
        'SELECT id FROM candidates WHERE email = $1',
        [candidate.email]
      );

      if (existing.rows.length > 0) {
        candidateId = existing.rows[0].id;
        console.log(`✓ Candidate already exists: ID ${candidateId}`);
      }
    }

    // Step 2: Insert candidate if new
    if (!candidateId) {
      const result = await client.query(
        `INSERT INTO candidates
         (first_name, last_name, email, phone, position, skills, source, location, current_position, current_company, tags)
         VALUES ($1, $2, $3, $4, $5, $6::text[], $7, $8, $9, $10, $11::jsonb)
         RETURNING id`,
        [
          candidate.first_name,
          candidate.last_name,
          candidate.email || null,
          candidate.phone || null,
          candidate.position,
          candidate.skills || [],
          candidate.source || 'LinkedIn - Sourced',
          candidate.location,
          candidate.current_position,
          candidate.current_company,
          JSON.stringify(candidate.tags || {
            sourced_by: 'coco',
            sourcing_run: new Date().toISOString().split('T')[0],
            profile_url: candidate.profile_url || ''
          })
        ]
      );

      candidateId = result.rows[0].id;
      console.log(`✓ Inserted candidate: ID ${candidateId}`);
    }

    // Step 3: Insert application with status='new'
    const appResult = await client.query(
      `INSERT INTO applications
       (candidate_id, job_id, status, notes, ai_recommendation, ai_screening_summary)
       VALUES ($1, $2, 'new', $3, $4, $5)
       RETURNING id`,
      [
        candidateId,
        jobId,
        'Passive sourced candidate -- confirmed interest via LinkedIn DM.',
        'Sourced candidate -- pending CV review',
        `Sourced on ${candidate.tags?.sourcing_run || new Date().toISOString().split('T')[0]} from ${candidate.source || 'LinkedIn - Sourced'}. Profile: ${candidate.tags?.profile_url || ''}`
      ]
    );

    const applicationId = appResult.rows[0].id;
    console.log(`✓ Inserted application: ID ${applicationId}`);

    await client.end();

    return {
      success: true,
      candidateId,
      applicationId,
      status: 'new'
    };
  } catch (error) {
    console.error('Error inserting candidate:', error);
    await client.end();
    throw error;
  }
}

/**
 * Parse CLI arguments
 */
function parseArgs() {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--')) {
      const key = process.argv[i].substring(2);
      const value = process.argv[i + 1];
      if (!value?.startsWith('--')) {
        args[key] = value;
        i++;
      }
    }
  }
  return args;
}

/**
 * Main execution
 */
async function main() {
  const args = parseArgs();

  if (!args.name || !args.url || !args.jobId) {
    console.error(`
Usage:
  node insert-confirmed-candidate.js \\
    --name "First Last" \\
    --url "https://linkedin.com/in/..." \\
    --jobId 123 \\
    --company "Current Company" \\
    --position "Current Role" \\
    --location "City"
    `);
    process.exit(1);
  }

  const [firstName, lastName] = args.name.split(' ');

  const candidate = {
    first_name: firstName,
    last_name: lastName || '',
    email: null, // LinkedIn sourced candidates often don't have email
    phone: null,
    position: args.position || 'TBD', // Target position at Taleemabad
    skills: args.skills ? args.skills.split(',') : [],
    source: 'LinkedIn - Sourced',
    location: args.location || 'Pakistan',
    current_position: args.position || '',
    current_company: args.company || '',
    profile_url: args.url,
    tags: {
      sourced_by: 'coco',
      sourcing_run: new Date().toISOString().split('T')[0],
      profile_url: args.url
    }
  };

  try {
    const result = await insertConfirmedCandidate(candidate, args.jobId);
    console.log(`\n✅ Success!`);
    console.log(`   Candidate ID: ${result.candidateId}`);
    console.log(`   Application ID: ${result.applicationId}`);
    console.log(`   Status: ${result.status}`);
  } catch (error) {
    console.error(`\n❌ Failed:`, error.message);
    process.exit(1);
  }
}

// Export for programmatic use
module.exports = { insertConfirmedCandidate };

// Run if called directly
if (require.main === module) {
  main();
}
