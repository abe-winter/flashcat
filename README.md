# flashcat

CLI tool which turns a wikipedia category into anki flash cards.

## getting credentials

Log in to the wikimedia API portal and create a personal access token using the 'Create key' button here https://api.wikimedia.org/wiki/Special:AppManagement.

Then make a json file like this with the result:

```json
{
	"client_id": "hexhexhex",
	"client_secret": "hexhexhex",
	"access_token": "base64.jwt_idk-longlonglong"
}
```
