import base64, sys
from pathlib import Path

def img_to_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Load logos
t_logo  = img_to_b64('C:/Agent Coco/assets/logo_taleemabad.png')
fb_logo = img_to_b64('C:/Agent Coco/assets/logo_facebook.png')
ig_logo = img_to_b64('C:/Agent Coco/assets/logo_instagram.png')
li_logo = img_to_b64('C:/Agent Coco/assets/logo_linkedin.png')

with open('C:/Agent Coco/invite_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the social icons table with real logos
old_social = '''            <!-- Social icons row -->
            <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:18px;">
              <tr>
                <!-- Taleemabad "T" logo circle -->
                <td style="padding-right:8px;">
                  <a href="https://taleemabad.com" style="text-decoration:none;">
                    <table cellpadding="0" cellspacing="0" border="0"
                           width="34" height="34" bgcolor="#2e7a4f"
                           style="border-radius:17px;">
                      <tr>
                        <td align="center" valign="middle"
                            style="font-family:Arial,sans-serif; font-size:14px;
                                   font-weight:bold; color:#ffffff; line-height:34px;">
                          T
                        </td>
                      </tr>
                    </table>
                  </a>
                </td>
                <!-- Facebook -->
                <td style="padding-right:8px;">
                  <a href="https://www.facebook.com/taleemabad" style="text-decoration:none;">
                    <table cellpadding="0" cellspacing="0" border="0"
                           width="34" height="34" bgcolor="#1877F2"
                           style="border-radius:17px;">
                      <tr>
                        <td align="center" valign="middle"
                            style="font-family:Arial,sans-serif; font-size:15px;
                                   font-weight:bold; color:#ffffff; line-height:34px;">
                          f
                        </td>
                      </tr>
                    </table>
                  </a>
                </td>
                <!-- Instagram -->
                <td style="padding-right:8px;">
                  <a href="https://www.instagram.com/taleemabad" style="text-decoration:none;">
                    <table cellpadding="0" cellspacing="0" border="0"
                           width="34" height="34" bgcolor="#C13584"
                           style="border-radius:17px;">
                      <tr>
                        <td align="center" valign="middle"
                            style="font-family:Arial,sans-serif; font-size:13px;
                                   font-weight:bold; color:#ffffff; line-height:34px;">
                          ig
                        </td>
                      </tr>
                    </table>
                  </a>
                </td>
                <!-- LinkedIn -->
                <td>
                  <a href="https://www.linkedin.com/company/taleemabad" style="text-decoration:none;">
                    <table cellpadding="0" cellspacing="0" border="0"
                           width="34" height="34" bgcolor="#0077B5"
                           style="border-radius:17px;">
                      <tr>
                        <td align="center" valign="middle"
                            style="font-family:Arial,sans-serif; font-size:13px;
                                   font-weight:bold; color:#ffffff; line-height:34px;">
                          in
                        </td>
                      </tr>
                    </table>
                  </a>
                </td>
              </tr>
            </table>'''

new_social = f'''            <!-- Social icons row -->
            <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:18px;">
              <tr>
                <td style="padding-right:10px;">
                  <a href="https://taleemabad.com" style="text-decoration:none;">
                    <img src="data:image/png;base64,{t_logo}" width="34" height="34" alt="Taleemabad" style="display:block; border-radius:17px;">
                  </a>
                </td>
                <td style="padding-right:10px;">
                  <a href="https://www.facebook.com/taleemabad" style="text-decoration:none;">
                    <img src="data:image/png;base64,{fb_logo}" width="34" height="34" alt="Facebook" style="display:block; border-radius:17px;">
                  </a>
                </td>
                <td style="padding-right:10px;">
                  <a href="https://www.instagram.com/taleemabad" style="text-decoration:none;">
                    <img src="data:image/png;base64,{ig_logo}" width="34" height="34" alt="Instagram" style="display:block; border-radius:17px;">
                  </a>
                </td>
                <td>
                  <a href="https://www.linkedin.com/company/taleemabad" style="text-decoration:none;">
                    <img src="data:image/png;base64,{li_logo}" width="34" height="34" alt="LinkedIn" style="display:block; border-radius:17px;">
                  </a>
                </td>
              </tr>
            </table>'''

html = html.replace(old_social, new_social)

with open('C:/Agent Coco/invite_template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Template updated with real logos.")
