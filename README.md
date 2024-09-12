# Giberish about project

Please do not try to test setup this project it will be annoying but continue if you feel like it

will be here womp womp

# Test Setup in docker

clone this repository:

```sh
git clone https://github.com/jansevounek/Password.git
```

Add to the .env files all the informations - good luck (you need to create accounts by some companies - these include stripe, supabase, ...) 

```sh
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

And that is basically it run:

```sh
sudo docker-compose up -d
```

That is it your server should be now running on port on localhost 8080.

# Test Setup normally

clone this repository:

```sh
git clone https://github.com/jansevounek/Password.git
```

Add to the .env files all the informations - good luck (you need to create accounts by some companies - these include stripe, supabase, ...)

```sh
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

The run (in the "Learner_frontend/" folder):

```sh
npm install
```

and then

```sh
npm run dev
```

Next go to the "Learner_backend/" folder and run:

```sh
python3 -m venv venv
source venv/bin/activate //on Linux
source venv/Scripts/activate //on Windows
pip3 install -r requirements.txt
```

After everything is installed go to the "Learner_api/" folder and run:

```sh
python3 app.py
```

Then go to the "Learner_scripts/" folder and run:

```sh
python3 app.py
```

Plus you are going to need to install the stripe [cli](https://docs.stripe.com/stripe-cli) and run the command 

```sh
stripe listen --forward-to localhost:5000/payment-successful
```

and that is it (not really look forward to some more supabase and stripe configuration tomfoolery)

Your development server is now running at the adress: http://127.0.0.1:5173/
