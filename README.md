# PyCosting
It's PyFecons, but with a different name. 

### Committing code
```bash
git add
git commit -m "Message"
git push
git pull
```

### Installing LaTex
https://github.com/James-Yu/LaTeX-Workshop/wiki/Install

### Creating a key pair
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/your_file.pub
```
Add to GitHub keys.


### Creating a virtual environment

```bash
# remove existing environment (on clean up)
rm -rf venv

# create virtual environment (on new environment)
python3 -m venv venv

# activate virtual environment (on new terminal)
source venv/bin/activate

# install dependencies (on new environment or after changes)
pip install -r requirements.txt


```


### Running the costing code
```bash
python3 RunCosting.py "CATF"
```
