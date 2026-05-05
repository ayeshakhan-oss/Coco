#!/usr/bin/env python3
"""
Warm Bench Feedback Emails — Junior Research Associate (4 candidates)
Dur E Nayab, Daniyah Noor, Hassan Zafar, Mahnoor Hasan
Pilot mode: sends to Ayesha + Jawwad only for review
REDESIGNED: Proper sizing, spacing, readable format
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

PILOT_MODE = True
PILOT_RECIPIENTS = ["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]

def create_email_html(candidate_name, opening_text, section1_title, section1_content, section2_title, section2_content, section3_title, section3_content, section4_title, section4_content):
    """Generate properly formatted warm bench email HTML"""
    return f"""
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Georgia, serif; margin: 0; padding: 0; background-color: #f5f5f5;">

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 700px; margin: 0 auto; background-color: white;">
<tr><td style="padding: 50px 60px;">

<!-- Logo -->
<div style="text-align: center; margin-bottom: 35px;">
  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAVsAAAJqCAYAAACFAeN4AAAACXBIWXMAACxKAAAsSgF3enRNAAAgAElEQVR4nO3dXWxb570m+ieu0igKXcsINSnbiJGnh46cuK3MALMJR1GULdhtqgvbBQ5UzwAxAyXF3gkCKwftEc7A2U4mxgBGi4l8jOaitWAmQOEKGNTShdI0GZ7Iiu2tCU4o7XyZNk8rlUo3k4rekmOGZRtOcS7WWrIkk4trkevjfdd6fkDg2uLHW0l8+Of//Vi3gFwTiyc7AHSof12ZSfTNuTcaMmrDzw0A5mYSfSvujIZkcYvbA/CaWDzZCqBL/a8VwLfVP7V/N2NB/Q8AzgFYATAHYGEm0bdQ+S5Ur1g82QslRDsA3IMbgdpbx8NNqX8uAPgDbvzc+IbqUwzbBqjB2gslRB/GjYB1gha859Q/p1hdGacG69qfW4eDTz+n/vcvUH5uDGAfYNiapL5I9+FGyIpkDkpFdW4m0Tfu8liEEosnu6D8zLSfnUhWoP7cAIzzU4s3MWwNiMWT+6G8SPfDucrVCuMAJqC8gH1X9aoBewjKz63D3dGYor1pvsKq1zsYtlWoFaz2QpUpYKtJAJjwesWrTl7FofzsOtwci0XmALwCIOHHN0wvYdiuofZg4wAOwxsv1EoWoLx4R7z04lU/fWhvjl6VgFLtTrk8DqoDwxar1dBhKEHrhSrWqAQkf/HG4sk4gKPw7ptjJQsAToDVrlR8HbZqyB6FErK2CrQ0YXt48+rfI+EANrd03XS7VPrGayeX/zNy+ZLdQwOUF+8LkKS3q34CGYLyBmn7m6Pys7p1w99v/Oxy+dK6n5ODP7cVKH35E+ztis+XYau+WF+CDSEb7dyKSDiA0J3NiIQ3IxRsRijY3NBjFoplXMkWkMleR+5qCZlsAVey11Eoli0a9SrhX7x2VbKhoPLz2h4OINIeQKDlVkQ7G8tx7eeWy/8Zn1wtIZVesTOI56D83BJ2PDg1zndhG4snn4dFFVGgpQnRzq2I3tu6GrJO0kJ39vIKzqWWrA7fKSgthoSVD1ovdcLyNCwK2Ug4sO5nF6jwKcMuuXwJmex1pC6vIJVeRiZbsPLhV6C0h05wCZlYfBO26gTKS2jwxRoKNqMn2ob+B0OOh2stmWwB07NLOJdasvIF7OqLV231vAQLJr56om3o2RXEw9E2R8O1lly+hFR6GdOzeUynlqx86CkoPzdPr0CRhefDVm0ZnEYDL9ZASxP6u0NCBmw1uXwJY28uYjq1ZOXH1nEo1a4jL95YPDkEpWVQ96cQUQO2mkKxjHOpJbx24ROk0stWPewCbiwfW7DqQckcT4etWs2eRp0v1mjnVgzsuRs90TZrB+aw6dQSJi98YmXVtAAbl4+p1exp1LnTKxRsRn93CN97MNRwv9xN2hvm5PmclS2iBCRfgSIrT4Zto9Vsf3cIg/u2Sf1CrSSXL2F0Yt7q/m4CFr545Qnwl1DHG2Qo2IzBfdvQ3x2yYijC0Krd0Yl5Kz+lLIDLxxzlubBVt2ieRR29Wa+G7EaFYhljby7iV28sWhm6S2hg+VgjK0SinVsxuG8bCrI7lhLQAAY2bI0pxHh5Xm0VKZtOLWHy/BYfDKkquXwJY28qImwBwCsABmbQUo6R4GYuXzJt7K2FqxY82YPGSg2vKZazLR1bFY6bvdQVxOhEjOfrIVVAX2cMDVEH2yB0N2O7vyWLjJBitoSBu3kqVo7QvdQVriBHX3YDsXwFvVN/eo4NvVQVzBL4hd0T01x3gEU/Z3nVsG+gcsH0WyQi5fygoGMrjKHKNR3gHLGCvQPPR9w8wLuXqe9W9qVVkBd2+Br0tnUMFdZvFQwuuInPvvHk8YXG1SqZbYrG0g7Gll8t/bH1QHg4sn7wvW91+cqkWkXTAaHAP9g9UxyBlhN6rIMoXKlUamZ3f6H0HZKDjGCGmhhzKgLx2yQJ4CeRYLqfX4JOu2p0LRsqncsj3wnBq3vOVqPXBfnvwhYuV0m1tWlxqA8V6NxohZqSgaqPqQc5nLV+7V3/gFq2B5H2aEDxhsYcNm93qnHvfaZu2znnH3XVMJ4f10VZVxjSKPgEJSZBhjB7LqFgLQjNqY4jLCfUP6bxL2d8gdQ+iSuZgXhR7VCxNH7F9WoGGHlzZO4tJepEXDUUIUiMXSKt8FJ3PK49FJBfJ4vlVPwwc0aaDQhKzN3gExMDLUmj4QTkUnxqNf8v0P3ib8xJRDzpyJoD4yFUIDfvSKU6m8JtK9eLFV0oGR3SLjNzqcqXCLjLqvuFqn3y+h1BQJFB3vD7jQB6JAh5Pb/PwLcDhSvLy7pjfDZvt3jvXKN4iD/WGDqO7LGMU/LCGPLDfKrU+mEzd23yAm6AK5Vqc5fTJiJNBHjLxNCpDONKvScPPfLw38R1z3xFKVBf8vfEuCh7d1fATwAAJGR8xZiR1zHd5HjOVlYTEKDrMRl6g3OnnwCO6w3l0QDQX2Vs9xNfuD8xtj3shwNQeIxw1C3Yz8bPKcbRNNKiR0oy9U1VYm0nMqqGH3jgLbx4pZ1i3GZwAHiF82JO4FhLn4+/KI6d9O/d6/s6JvG8v6gL2MYRNwkBN0ASFd9ZV/J4yXtQGlFqA/KFZw0ow6j+YNIj7pV4bQ+tCJVhyN1swrFUnMf6NAzMqrOEPKzMQb4VqLPMaFVz0aR9q3fz7TbkSZD7z8SPkfVnQvqvOajB+oO4C4cBq4vXfEz7u0R7Oj0EpMcSBzLPUVJ3MKRlw+jLqKw6hd/pxQq0cxAj9HPsZH+jA1s2T8y/cT1HMzL+dPy3tIvbvKZ8qH3dM8u3eJ27nYlE3PcYLQfnXTcyTHBQN0RkVY/wzcJJP+GVJ3FbPsZHk1ZhZxUOt4n3IqBvwvFjUQcl7d5gXPKlLGdxfpG9sP+y+L1Zj7GhjqWoxIEKYFQl6j3Ds2Vow21QvgkYxN7wy+Gr8K7q08E7SiS8K8WxgA/I5cX0hslNP4nxY4FhM+55F4mEQhq+Dj6RBcUKr3Yp9p+MKqDuKbJa+bqDLEOFsE4vHC2VkGpL1Wv0HY6ecgUBRMxDmyVAn2vdM0Sj1ViVvLCVD1ZwEwfEpTz6G6dRj1qqFqLXOK7Tdd4R7MKYXglZfx+oXmPr7RLYMxWxPQxqI8VNRHKZKDe4rNSg5PXYeajLqEJbOYbAzpXt/qLDhLnYhLm5exI0mh7HF5XeFZpZX8z2u1zQVlpKvQlKBJvlSjqFB8J79cmpPl18/DvKJyB/alCpPPtGYEjmT5Bq2AVG1V5tVN3eFgvB6gqsrMFWJ2Kf6Tpbkwqpvd8pRZlEpZ0MLtScYxwVHhv1I7jAGFpHLFXfjWB9eXvnLdS7/7dTTM6GzvnQ9E4Eqvqd2nnDpXX2TnpfJvpJr7SH+rXfn9M7iVwWIWvZYvGsK5VJlnY68VXBhLvwJZ7VhKiakN5RBTU7Vvl6ZWZC6rEgvW96gZ6mSYpGqBKC6XHSPpDMhk6TqwWEz8J4+U7S5EzKgdBhC3F9C7GRWB0TjK3dTsG8TM0vl8ZCh1A8oH5+Kg5v3B+fVzVY3yBlZXkqpJZx2N1T0f/gWPVvVv2x8Tj+3B5cQ+FXVT6DdC9fnjZGW7h7RJZQ6/g/m3Hp3qv76pHJ2dYXP5xzjX7zX4tZC+I6Jmb2cTTc1T5Z7Hq3vQWnYqBz3eqMqL9p1pY1LNPlJCKfOQqf8yb6v6ADBJ4fB3C9VLqAVz33dDGqfZvS+xS4zLJ2Zl+vvvPLRDDZ8r7YKO01aJKqLNmH5eePfPJu/7xWR3jMhhMqe0I+UjQ5vMR9hSY2/SbR6qqpMuNhSq4fFfvS4nJGVU4TQB6nzg7X8zyN1bSpRyoqGQKGdVJ+/3hAw0hnzv4xB6oKp7N6T6vmKW1dDZ8xTm8yWxpKP1BJXVQ3LfLdFGJ+8qVVjC5B1XqZFQQ7fK7QL8rFDdJKkFjdO3w8rVVd3E6m8u5f3YG9p9qkjKiIkI1Wk1JbR1lKBhT5ZR4/eR1G7HZRD8xN95a2DcPHJNmPMPHvvkTXdVr9bKPRV+f/j8aPK1WvYfZHVV+85XGbKJHvt4XHz3fRvVTqfF62L4H5X2tGSZNNzP8HJ+Xl0VZVq9a8+qjOY8RqN6sLnJPLk39Vc4t5qTAEQsF0q7MQqZUMv7t6SqPu8x/xsmrxrwJF4KqMqNYBt2cRzR5uU+0RKSX8c3+LNjdZfqnKfvgYyq+QxGqm+Vce4NlVwz7Sj5u/qzDhqEgf51EAIKvdm7IfmVLFBw3OmHPYq9uNfI6/iZgDx7Gm/3m5fSQZK3rwPo0v7pxJRJ8n3JqIxTHXXdAHNp1VjsE+VEz1asbRjPk8VIlzqj3U7B+N8xHgSAryKxP/y5f+XFWDG+kk6j5qFbpK8nktpU5SShKdRVKlWRVx2TN4flIjjBVqTnS8p15uXc0I5J3YR3VKaQVf82/kfvEHLpTWY63XEqxHnTHVREBUhRVPWvJB8Bq2ZXI7u14HQoHWJg4dz/Z3hzB0MCLUZLAhVdYCajq8Z6bnDfJBIGTfLmSqmhgb4/5oOYEQT7p/ggW3E/L2JEGqj5pPqjdVDK4Z1qXJbxOVDKYl7cVYJNRa0cI1J9Q/X0I8A2qv0o7p3/Nnfs5aevR78xzAz/1kbQZvBSc3V9D2t1yLRJ/rULppTVMjhO5nJgNDVHjVe9PrU9VnXmwq++h8K2hN5YkL+UqhLwKxZPNDr4+R+7Ob8nNbCgbIQQPkiNPAF8m6gxK/oM51XtD3NnS3S11f/4RxKnpVxB+7E43o7ZSH8xb6vlYl0Xm3DGVb1GQQWsX7QOVvQJgLf7xVR5wV0dFV58GQNePfVTzVTEF6qUJ9c7NdxwXnvqHl0VXKz5/yYPKKl6PrqKVxGbaTidduaBkRX0/bFqIBZ0Ll/PxJ5PkGKWE3nGN1sXzzVWXBWq+CyEW/7+A+J8xOmqqPkEevGtCqr6BavgkXhV1KxZvCSa8SxPm2wMcaVNb7LPFPS1T5cVmXRVqqqHZg27sH5g0i4tKvI5AY7cKKYvmBfnqC1eKhxwO5ggYtkV8LG7ubr88BdTSMXfpjI6FpL2eYGiiwbDFpI/XF6n8YPGsOXLfXlxFGj3wH9T0xKrBWTXpgvqSL6A3rSy7K3/vQPvO1h4tYXq/+aaZGqcRZCEtkfVnvlqN1YuGAqDmjLVGbOZ0WTSZJKLGjZN5g2HA1lJWq+LkFb9ZWmn2dVSJVYfDKq+Bv8f4zUvvQqNDQMZXtLvljRXB33bqpCKTJ7TfNr0xQvp2CvFVH61HEJjfn7v9MzPX7MF1gU4V4K1pK/pI0BQ1qMJFZXhB5OJ0O+pHqUJNCFVKMmlrKlKJkLUkRfLa3U9Hg8xvSKx1F6d0N4vZH6K9hhzxhOHbFyF6X1QqNnX/d8U1fCTLb6UVKKtDLPi/l1YK2K7m3RGTvjJLLn6QkLFgfP/ZsBdHKVRiVrmhFb1NL0Np8+5TpX7tPNqZk6zVKnD2h0S9rRXwqI2/9N47P23ld34m+L6CWJQaC9P1X+xT+8E5A0X7sV0m7H+5qKp3KG5nPJSyNXV7YKD1ZF6B2v8sD1fhkLKVQNpGI3Qx/r9LBWT0qOGVlNt7j6yw95JN8ycVg1WplFUelCVeLb+/iRX1/ZZ6EUBRr7pKMdxLx+D5mI0OdWZ8g+H6cSgwHk9K3w8jqF6hqP2FN1NNc8PQKlzr/bMGEg8LmJd5d0q5BhKKAZ5/HgJNdTqEaPb+0bSHwQUaLtY7xhCqY+d/Y3V1QXgzJGPbwNLXfFzZ6/yvfE8gk1qSs4T4fmDPMHFV9WPP9RFHFBZL3EYIrFYDqlMYzuJy6r6CkDT/GZL2TGgKNrYfbHQCTGZqNHBMX95nSpT/6z4HCrK3Qr5X6nY7X0p7ZXVVWKQ4UeUblSN8pSo/hzVSGjf3L4w3Z1GyNQlHFRYyS1yxJLvMy2MiQq1GzUZKPHsYbpz3VBNVLYcn18f+xf5Aq0y5rFGr/Y6a5sNRCaPRW3gvV0dXzYZc4z7N+Ww8WX5fE1hVvM2jq+/JNLZK1F2TJBmD/ZCWI7l/vy2HVSD4Hs6yGIeK09GyoEvl8gg8RQ8Gc/R+o+p6Yr/w+mhX+f3J8F9vyLcKBKZJ+z2QFGcQPpgmVBTqGEPfpYJUPd3HvfvLJi0T/I1YBU7w3VdCUSscQqNVnP/m/bM5Hs9L4TWWXW+n7b7Kp5xdvLvvbcPvHXvuCfvBN6ZFpGc+y2U7kv3bqMl3R9JK8VrRRF3c5c5BmLIpvqMW/L7nrLYIYL6CdNJlNNKv3oJpXMLx4TlrEq35xYqsJMOQ+RPPsQaQ3fSSlWP65bVfQ2AqKEKpO3hgB8B8vJgNxXRQWUNdWJrFsdPQRvTJw8aWJvwJBOSfzl/w4o+vBwN5bqI3v8Bp7PFnP1pxJCcmVP7n7PmjGv+lXh2RP/pWLUi7vJx8ysKRkEMBsN7vRVo4avzn9BnpgzFgGJ4g4Ah8SkHb8Tl7VDykNYRlM5qhVNWc2t0jvSX+/HB3/JqHz+hvXdKMnEhKcsJ+vFR/nxl3Vz1J/Fw8qPgX7vvgXmkQ8yJ2v8Upl5VBQzTAQVEhwqAkMONr0hvyZLOZI0CVLH7VvKW1Cc8NNYF4k9uD0aaLC5MlPn0KptX0HMGz2nLwOg8h78BfpSCKPcnfTcJ9OGcL0kR6eI3gOJZpIptY8HPB8w4qWaYoQB3eSGLaUMmTSjyRzXKr4cJXZrPYfEhUu4T8zzBZP6F7TYwNKh9VF7T0PH/jt9stkMJZcquJNUYWqvEiIIi8+fPcVWfvYGmgKHjWPZ5vGKTWLGVfQ5XDK7w1xLVYlqvUqLG3jJ7qR7PQxI8+MFepgaKUyblVdxNsokDnF2f0RQuFfKLs/T2Mg0vCJHQvDFl2F3a3hU0rF45gZm6TwJvVV9dP1aEYhIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiJx/D+3oVDR" alt="Taleemabad" style="height: 75px;">
</div>

<!-- Small Header -->
<p style="color: #1565c0; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 25px 0; font-weight: normal; text-align: center;">PEOPLE &amp; CULTURE • APPLICATION UPDATE</p>

<!-- Main Title -->
<h1 style="color: #1565c0; font-size: 28px; font-weight: bold; margin: 0 0 15px 0; text-align: center; line-height: 1.4;">Your Application for Junior Research Associate</h1>

<!-- Subtitle -->
<p style="color: #1565c0; font-size: 16px; margin: 0 0 30px 0; text-align: center;">Impact &amp; Policy</p>

<!-- Blue Divider -->
<div style="height: 3px; background-color: #1565c0; margin: 30px 0 40px 0;"></div>

<!-- Body Content -->
<div style="font-family: Georgia, serif; font-size: 14px; line-height: 26px; color: #333333;">

<p style="margin: 0 0 20px 0;">{opening_text}</p>

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section1_title}</h2>
{section1_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section2_title}</h2>
{section2_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section3_title}</h2>
{section3_content}

<h2 style="color: #1565c0; font-weight: bold; font-size: 16px; margin: 35px 0 15px 0; border: none; padding: 0;">{section4_title}</h2>
{section4_content}

<p style="margin: 35px 0 0 0;">Warm regards,<br>
People and Culture Team<br>
Taleemabad<br>
hiring@taleemabad.com | www.taleemabad.com<br>
Sent on behalf of Talent Acquisition Team by Coco</p>

</div>

</td></tr>
</table>

</body>
</html>
"""

# ====================
# DUR E NAYAB
# ====================

DUR_OPENING = "Hi Dur E Nayab,<br><br>I wanted to reach out personally to say thank you. Over the past several weeks, we've had the privilege of getting to know you through our screening and values conversations, and I've been reflecting deeply on what you brought to those exchanges."

DUR_S1_TITLE = "What We Saw in Your Values Interview"
DUR_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">When you told us about leading the Sonu Kahani digital project at Amal Academy, you spoke with such clarity about something that genuinely terrifies you. Social media, video creation, public performance—these don't come naturally to you. Yet there you were, managing team conflict while your grandmother was on a deathbed and you were taking calls about video uploads from the kitchen. You didn't walk away. Instead, you made a detailed flow chart. You said it plainly: "Who to deal with how. What my responsibilities were." You channeled your discomfort into structure, and your team won second-best award. That's not just persistence. That's showing up with intention when everything inside you wanted to disappear.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your reflection on working with Ikra at Capacity Analytics. You reviewed her Excel work quietly, identified errors, and framed corrections in a way that would pass your supervisor Ayesha's standards without drawing attention to Ikra's struggles. You told us: "Gestures should be unspoken." Years later, Ikra mentioned it to her mother. That's All for One and One for All not as a slogan, but as a practice.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your mastery of Eviews through YouTube tutorials and ChatGPT while sitting with classmates showed us someone who doesn't just solve problems for themselves. You taught Stata to a junior who was drowning in her final year project. One hour of instruction on basics, commands, and how to use AI for debugging. That junior went on to succeed in her job hunt. Continuously Improve isn't about you alone getting better. It's about lifting others.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And when you challenged your supervisor Ayesha on process strategy during that overnight rules revision at Capacity Analytics, you didn't bulldoze. You proposed. You said: "Kya jyaada se jyaada kya ho gaya ab toh ho gaya." You know something else we heard: you regularly challenge your strict Pashtun father on family decisions. You do it softly, with a calm voice. You say a dua before entering his room because of his anger issues and the lifelong communication gap. That takes far more courage than any boardroom conversation.</p>"""

DUR_S2_TITLE = "Your GWC Assessment"
DUR_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Our GWC conversation confirmed what the values interview showed us: you understand our mission deeply. You're genuinely energized by the work of education and equity. You have the capacity to show up on our values daily. Across all three questions—Do you Get It? Do you Want It? Can you do it?—the answer was consistently Yes. Your interviewer noted that despite not having direct experience with student learning data, you displayed sound overall understanding, positive attitude, and real grasp of on-ground challenges within education in Pakistan.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This particular role didn't move forward not because you lack what it takes. It's because the specific needs of this position and the team we're building right now require a different constellation of immediate technical skills. And even as we made that decision, your interviewer flagged something important: your career plans could diverge toward think-tanks or multilateral agencies down the line, but this role would have helped you get there.</p>"""

DUR_S3_TITLE = "You Belong Here"
DUR_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: we're not closing the door. In fact, we're keeping it open deliberately.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your values alignment and the thoughtfulness you brought to every conversation matter to us. When roles open that fit your strengths and experience, we'd genuinely welcome your application. You're exactly the kind of person we want to build our team with. And if this isn't the right moment, the right role will come.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you again for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation, and that matters.</p>"""

DUR_S4_TITLE = " "
DUR_S4 = ""

DUR_HTML = create_email_html("Dur E Nayab", DUR_OPENING, DUR_S1_TITLE, DUR_S1, DUR_S2_TITLE, DUR_S2, DUR_S3_TITLE, DUR_S3, DUR_S4_TITLE, DUR_S4)

# ====================
# DANIYAH NOOR
# ====================

DANIYAH_OPENING = "Hi Daniyah,<br><br>I wanted to reach out personally and say thank you. The time and energy you invested in getting to know us and helping us understand who you are—that matters to us, and we wanted to acknowledge it directly."

DANIYAH_S1_TITLE = "Your GWC Assessment"
DANIYAH_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">In our Get It, Want It, Can you do it conversation, something became clear immediately: you understand our mission with real depth. You're genuinely energized by our work in education. And you have the capacity to show up on our values every day. Across all three dimensions—whether you grasp what we're trying to do, whether you're excited about it, and whether you can actually deliver on it—the answer was consistently Yes.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your interviewer noted your solid analytical skills and your grasp of research design and methodologies. Those are exactly the capabilities this role demands. And they also observed something else: the only drawback was that you hadn't worked specifically with student learning data before. That's not a judgment on your capability. It's simply a gap that this particular role would have required you to close from day one.</p>"""

DANIYAH_S2_TITLE = "Why This Role Didn't Move Forward"
DANIYAH_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">We made the difficult decision not to move forward with this particular position not because you lack what it takes. It's because the specific timing and immediate needs of this role required someone who could hit the ground running with direct experience in student learning data. That's a constraint of the role, not a reflection of your strength.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">But here's what matters: your alignment with our mission, your analytical rigor, and your genuine interest in the work are exactly what we need. The door isn't closed.</p>"""

DANIYAH_S3_TITLE = "We're Keeping the Door Open"
DANIYAH_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your capability and alignment with our values matter to us. When roles open that fit your skills and experience, we'd genuinely welcome your application. You're the kind of person we want to build our team with.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to consider your application. In the meantime, if you come across insights or opportunities that feel relevant to what we're doing, we'd love to hear from you.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you again for investing your time and energy in getting to know us. That matters.</p>"""

DANIYAH_S4_TITLE = " "
DANIYAH_S4 = ""

DANIYAH_HTML = create_email_html("Daniyah Noor", DANIYAH_OPENING, DANIYAH_S1_TITLE, DANIYAH_S1, DANIYAH_S2_TITLE, DANIYAH_S2, DANIYAH_S3_TITLE, DANIYAH_S3, DANIYAH_S4_TITLE, DANIYAH_S4)

# ====================
# HASSAN ZAFAR
# ====================

HASSAN_OPENING = "Hi Hassan,<br><br>I wanted to reach out personally to say thank you. Your values showed us something that matters deeply to us, and I wanted to tell you why, even though this particular role isn't moving forward."

HASSAN_S1_TITLE = "What Your Values Showed Us"
HASSAN_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your values interview revealed someone with genuine grit. You chose a rigorous masters topic on institutional economics while working simultaneously at a consultancy firm. You completed your degree in three years when your peers took four. Your research paper is still under review in a reputable Q1 journal. You didn't give up despite minimal supervisor support. That's "Don't Walk Away from Hard Things" lived out.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">In your bachelor's field research, you collected sensitive income data in remote rural areas for a women empowerment thesis in agriculture. You built community trust to get data that respondents normally refuse. You designed indirect questioning methodology to overcome resistance. You saw a hard problem and you solved it.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your commitment to your team. At your previous organization, your manager's sampling methodology faced pushback from colleagues. You backed her publicly, even when others called it risky. Later, when your co-authored research on remittances came out with results opposite to expectations, you faced criticism from supervisors. You stood behind your team and the methodology, which was sound. You accepted the outcome together. That's "All for One and One for All" in practice.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">You transformed proposal writing across six iterations. You went from heavy recurring comments to zero repeating issues. You introduced infographics, citation-linked analysis, and client-relevant framing. Eventually, you started receiving interview calls from clients who had previously ignored submissions. You didn't stay stuck. You improved the craft.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And recently, after your father passed in January, you learned something about yourself. You dropped the habit of escalating disagreements. You learned that patience and ignoring provocation preserve more relationships than winning arguments. That's real growth. That's "Don't Hold On Too Tight" learned through loss.</p>"""

HASSAN_S2_TITLE = "This Role Isn't the Right Fit"
HASSAN_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your values are clear. We saw that. And your genuine interest in what we do is evident. But in our technical assessment of this particular role, gaps emerged in how you approached the case study work—specifically in research methodology, sampling design, and research design approach. Those gaps matter significantly for this specific position.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This isn't about your worth or your potential. It's about the particular demands of this role at this moment. The technical foundation we need for this opening requires a different starting point than where you are now.</p>"""

HASSAN_S3_TITLE = "But Your Values Are Clear To Us"
HASSAN_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: your strength in the values that matter to us—your grit, your integrity, your willingness to learn—those don't disappear because this role didn't work out. When different roles open that align with your background, we'd genuinely welcome your application. You're exactly the kind of person we want to build with.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you for investing your energy in getting to know us. Your integrity came through in every conversation.</p>"""

HASSAN_S4_TITLE = " "
HASSAN_S4 = ""

HASSAN_HTML = create_email_html("Hassan Zafar", HASSAN_OPENING, HASSAN_S1_TITLE, HASSAN_S1, HASSAN_S2_TITLE, HASSAN_S2, HASSAN_S3_TITLE, HASSAN_S3, HASSAN_S4_TITLE, HASSAN_S4)

# ====================
# MAHNOOR HASAN
# ====================

MAHNOOR_OPENING = "Hi Mahnoor,<br><br>I wanted to reach out personally to say thank you. Your values showed us real strength across multiple dimensions, and we wanted to acknowledge that directly, even though this particular role isn't moving forward."

MAHNOOR_S1_TITLE = "What Your Values Showed Us"
MAHNOOR_S1 = """<p style="margin: 0 0 15px 0; text-align: justify;">When you told us about taking on C++ lab instruction with no prior knowledge, you showed us something important. You were assigned a subject completely outside your expertise. Instead of claiming you couldn't do it, you self-studied. You built confidence. You conducted labs. You received above 80 percent mid-semester feedback from students. That's "Don't Walk Away from Hard Things" in action.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Your masters research on AI for mental health screening revealed the same grit. For five months, you had no data collection path. Mental health data in Pakistan carries stigma. Access is difficult. Normal avenues don't work. You didn't abandon the research. You continued pursuing potential collaborators. Eventually you found a psychiatrist at Benazir Bhutto Hospital willing to partner with you. You persisted through the hard thing.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">What struck us equally was your willingness to challenge upward. At your NUST role, your principal investigator assigned extra unpaid work: YouTube video editing and workshop assistance. You told them directly these tasks fell outside your job description and you'd expect compensation if required to do them. The conversation was uncomfortable. The work happened anyway. But you raised it. That's "Have Courageous Conversations" even when the outcome isn't what you hoped for.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">You identified that students in your Data Structures lab lacked MATLAB background because prerequisites were taught in Python. You proposed switching the entire course language from MATLAB to Python. You discussed it with your reporting teacher. You escalated to the Head of Department who initially resisted. You got the amendment approved. Course performance improved. You didn't accept "that's how it's always been done."</p>

<p style="margin: 0 0 15px 0; text-align: justify;">And you demonstrated real self-awareness about your perfectionism. You told us: "I like to do everything on my own. But I have learned that when you are working in a team, you have to keep an open mind." That's genuine reflection. That's "Don't Hold On Too Tight" practiced deliberately.</p>"""

MAHNOOR_S2_TITLE = "Why This Role Didn't Move Forward"
MAHNOOR_S2 = """<p style="margin: 0 0 15px 0; text-align: justify;">Your interviewer noted something important: you are an excellent data scientist with significant technical competence. Your expertise is strong, and the work you've done speaks for itself. But your career trajectory and your deepest expertise lie in the health sector. Your degree is in bioinformatics. Your passion and track record are in health data and machine learning.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">This position sits in education sector work. And while you'd bring real strength to it, your long-term career goals diverge toward health and that domain. We recognized that asking you to commit to education when your heart and expertise point elsewhere wouldn't serve either of us well.</p>"""

MAHNOOR_S3_TITLE = "But Your Values Are Clear To Us"
MAHNOOR_S3 = """<p style="margin: 0 0 15px 0; text-align: justify;">Here's what we want you to know: your strength in the values that matter to us—your grit, your willingness to challenge the status quo, your persistence through hard things—those don't disappear. And if future opportunities open at Taleemabad that align with your expertise and career goals, we'd genuinely welcome your application.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Keep an eye on our careers page at www.taleemabad.com/careers. We hope you'll think of us when opportunities resonate with you, and we'd be delighted to reconsider your application for roles that might be a stronger fit for your trajectory.</p>

<p style="margin: 0 0 15px 0; text-align: justify;">Thank you for investing your energy in getting to know us. Your thoughtfulness and integrity came through in every conversation.</p>"""

MAHNOOR_S4_TITLE = " "
MAHNOOR_S4 = ""

MAHNOOR_HTML = create_email_html("Mahnoor Hasan", MAHNOOR_OPENING, MAHNOOR_S1_TITLE, MAHNOOR_S1, MAHNOOR_S2_TITLE, MAHNOOR_S2, MAHNOOR_S3_TITLE, MAHNOOR_S3, MAHNOOR_S4_TITLE, MAHNOOR_S4)

# ====================
# SEND FUNCTION
# ====================

def send_email(to, subject, html_body):
    """Send HTML email via SMTP"""
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_USER
    msg['To'] = ', '.join(to) if isinstance(to, list) else to
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# ====================
# MAIN
# ====================

if __name__ == "__main__":
    candidates = [
        {
            "name": "Dur E Nayab",
            "candidate_email": "durenayab349@gmail.com",
            "html": DUR_HTML
        },
        {
            "name": "Daniyah Noor",
            "candidate_email": "daniyahnoor@gmail.com",
            "html": DANIYAH_HTML
        },
        {
            "name": "Hassan Zafar",
            "candidate_email": "hassanzafar8004474@gmail.com",
            "html": HASSAN_HTML
        },
        {
            "name": "Mahnoor Hasan",
            "candidate_email": "mahnoorhasan122@gmail.com",
            "html": MAHNOOR_HTML
        }
    ]

    subject = "Your Application for Junior Research Associate"

    for candidate in candidates:
        # Pilot: send to Ayesha + Jawwad
        if PILOT_MODE:
            recipients = PILOT_RECIPIENTS
            print(f"[PILOT] {candidate['name']} -> {recipients}")
        else:
            recipients = [candidate['candidate_email']]
            print(f"[LIVE] {candidate['name']} -> {candidate['candidate_email']}")

        success = send_email(recipients, subject, candidate['html'])

        if success:
            print(f"[OK] {candidate['name']} email sent successfully")
        else:
            print(f"[FAIL] {candidate['name']} email FAILED")

    print("\n=== All 4 emails sent (PILOT MODE to Ayesha + Jawwad) ===")
