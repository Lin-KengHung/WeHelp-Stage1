# week6 asignment 

## Core-concept and Solution
### user status part
1. user status are recorded by signed cookie-base session (all of information are set at signed cookie), name is cookie-token
2. signer: python package "itsdangerous"
3. if cookie was modified, return error message 
### submit message part
4. when render all message in member page, "message id" were recorded in id attributes in a specific html element by html template input value
5. "username" were also recorded in a specific html element
6. trash button were be replace to another html element if username != username in cookie. The logic is judged by html template when render
7. back-end also checked whether message want to be delete is belong to himself/herself

## User flow
![wehelp_week6_userFlow drawio](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/2bfa49bf-44f5-4a84-ad53-475e840be6f6)
## ERD
![ERD](https://github.com/Lin-KengHung/WeHelp-Stage1/assets/80440675/e49627c4-4310-48fb-b746-5f090007d43d)
