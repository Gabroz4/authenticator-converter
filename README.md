python program to convert proton authenticator unencrypted json export to a bitwarden authenticator compatible 2fas schema

how to use: 

- export from proton authenticator to "simple text"
- clone this repo and copy the file inside the folder

- run: 
  - python3 converter.py your_exported_file.json.txt 2fas_conversion.json

- import to bitwarden authenticator as 2fas jso file

Feel free to inspect the code manually or with AI, this program just does a simple text transformation, no internet requests or scammy stuff.
I just needed this tool for myself so why not help someone else, enjoy ;)
