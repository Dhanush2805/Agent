import subprocess
import sys
import os

ALLOWED_DOMAINS = [

    "@gmail.com"

]

########################## FETCH COMMIT EMAILS ###########################

def get_commit_emails():
    try:
        cmd = [
            "git",
            "log",
            "origin/main..HEAD",
            "--pretty=format:%ae"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        emails = list(set([
            email.strip()
            for email in result.stdout.split("\n")
            if email.strip()
        ]))
        print('email_found========',emails)
        return emails

    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        sys.exit(1)

####################### VALIDATE EMAIL DOMAINS################################

def validate_email_domains(emails):
    invalid_emails = []
    for email in emails:
        valid = False
        for domain in ALLOWED_DOMAINS:
            if email.endswith(domain):
                valid = True
                break
        if not valid:
            invalid_emails.append(email)
    return invalid_emails

################################ MAIN#########################

def main():

    print("Running Rule-Based Domain Agent")
    before = os.getenv("GITHUB_EVENT_BEFORE")
    after = os.getenv("GITHUB_SHA")
    emails = get_commit_emails()
    print("\n📧 Emails Found:")
    for email in emails:
        print(f" - {email}")
    invalid_emails = validate_email_domains(emails)
    if invalid_emails:
        print("\n❌ Invalid Emails Detected:")
        for email in invalid_emails:
            print(f" - {email}")
        print("\n AGENT FAILED")
        sys.exit(1)
    else:
        print("\n All emails are valid")
        print("AGENT PASSED")

if __name__ == "__main__":
    main()
