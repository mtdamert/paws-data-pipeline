The logic for looking at duplicates from Karla/Meg discussion:

1. Create Matches from Salesforce
2. Compare Volgistics to Matches: If [fuzzy match on name above threshold] and [match on email] → combine records in Matches
3. Compare Matches to PetPoint: If [fuzzy match on name above threshold] and [match on email] → combine records in Matches
4. Compare Matches to ClinicHQ: If [fuzzy match on name above threshold] and [match on phone number] → combine records in Matches

Trigger staff review: If [fuzzy match on name above threshold] and [no other matching data] → report for human review

Thresholds are TBD but should be some level where we can be reasonably certain the fuzzy match is correct most of the time.
Decided to trust name and email most. Addresses will likely create more problems with fuzzy matching, allowing people in the same household (but not the same person) to potentially be matched. Email is likely to be unique per person, though the same person *may* use multiple emails. 
