# 100aedes - Project

An app to help citizens in the fight against mosquito Aedes aegypti.

The `master` branch is deployed to 

- **Staging server:** [Official server](https://100aedes.com.br/) - DigitalOcean

The `development` branch are deployed to 

- **Staging server:** [https://staging.100aedes.com.br/](https://staging.100aedes.com.br/) or [Heroku Direct Link](https://100aedes.herokuapp.com)

- **Local server:** follow steps how to run in vagrant with ansible.

# Technologies used

- **Frontend:** Bootstrap 4, SASS, Gulp (Automate tasks) and AngularJS 1.5x

- **Backend:** Python/Django, Django Rest Framework(API) and Unit Tests

- **Infrastructure:** Ansible (IT automation), GUnicorn, NGINX, Supervisor and Digital Ocean Management.

## Installation

### Configuring Ansible

First of all you need to have Python 2.7 installed, because Ansible only works with this python version.

After, install ansible (Make sure that you have pip installed)

```
$ pip install ansible
```

So, clone this repository

```
$ git clone https://github.com/leonardocouy/100aedes
```

Go to the ansible folder located in root project dir and run commands below

```
$ cd ansible
```

##### Ok, now **IT'S TIME!!**
Provision local machine with vagrant

```
vagrant up
```

**ACCESS YOUR DJANGO APPLICATION BY GOING TO THIS URL: **[http://192.168.4.23](http://192.168.4.23)

Re-provision the box to apply changes.

```
vagrant provision
```

**SSH to the box**

```
vagrant ssh
```

#### Some details about this Ansible Playbook can see in this repository: 
- [DjAnsible by Leonardo Flores](https://github.com/leonardocouy/djansible)

### Configuring the Project

1. Copy .env sample and fill the required fields
	- `cp contrib/env-sample .env`
2. Generate a new secret key and copy&paste to .env
	- `python contrib/secret_gen.py`
3. Create a virtualenv using Python 3.5
	- `python -m venv venv`
4. Activate virtualenv
	- `source venv/bin/activate`
5. Install requirements
	- **Dev:** `pip install -r requirements/dev.txt`
	- **Staging:** `pip install -r requirements/staging.txt`
	- **Production:** `pip install -r requirements/production.txt`
6. Migrations
	- `python manage.py makemigrations --settings=backend.settings.dev`
	- `python manage.py migrate --settings=backend.settings.dev`
7. Install NPM Modules (includes Gulp) and automatically will build dist package
	- `npm install` 
8. Run collectstatic
	- `python manage.py collectstatic --settings=backend.settings.dev`
9. Run tests
	- `python manage.py test --settings=backend.settings.dev` 
10. Run server
	- `python manage.py runserver --settings=backend.settings.dev`


### How to deploy? (Ansible)

Provision the staging server

```
ansible-playbook -i hosts staging.yml
```

Provision the production server

```
ansible-playbook -i hosts production.yml
```

### How to test?

```
python manage.py test --settings=backend.settings.dev` 
```
