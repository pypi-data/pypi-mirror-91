
<h2 align="center">Docker-based CI/CD made easy</h2>

<p align="center">
<a href="https://travis-ci.com/numericube/dmake"><img alt="Build Status" src="https://travis-ci.com/numericube/dmake.svg?branch=master"></a>
</p>

Dmake is the missing link between Docker and your Cloud Provider \(AWS / Azure / other\).

**Dmake makes Docker and cloud-based CI/CD easy:**

* Start your projects with CI/CD built-in
* Stop spending hours tuning your docker-compose configuration files
* Collaborate with your fellow developers ensuring your environments are all the same \(ie. no more "it worked on my local machine but not on the server"\)

## What can dmake do for me?

Dmake is a frontend to Docker+Swarm, providing sensible defaults for usual CI/CD tasks such as:

* keeping track of various environments \(dev/test/prod/etc\)
* managing releases and deployments
* performing day-to-day operations on a Swarm cluster \(eg "I want to run this piece of code on that environment"\)
* ...and do all of this with AWS or Azure clusters!

We are making a few assumptions for now:

* We use Docker \(obviously\)
* We use docker-compose because it's the right tool for this job.
* We use Swarm. We know this is a controversial choice but we plan to move the whole project to Kubernetes. In the meantime... ...sorry: Swarm.
* We assume your repository is hosted on Git 🤷‍
* Your provision configuration is stored in the 'provision/' directory by default \(customizable\)

## See it in action

### How to write docker-compose.yml files?

Without `dmake`:

```...hours of fiddling, docker-compose start/stop commands with ever-growing parameters...```

With `dmake`:

```
$ dmake config
```

### Start a multi-environment docker-compose stack

Without `dmake`:

```
$ DEPLOY_ENV=dev docker-compose -f my-project/docker-compose.yml -f my-project/docker-dev.yml start
```

With `dmake`:

```
$ dmake stack start
```

### Creating a multi-environment setup (dev / test / staging / prod)

```
$ dmake config --env=test
$ dmake config --env=staging
$ dmake config --env=prod
```

### Execute a command inside a specific container of your running stack

```
$ dmake stack exec /bin/bash
```


## General principles

dmake makes your development, releases and deployment operations WAY simpler and streamlined with Docker+Swarm.

It practically makes your project fool-proof for users who don't know or do not want to learn all about Docker.

But it allows power users to save time and energy by providing convenient frontends to most operations.

The only thing you have to do is describe your project architecture in the 'provision/' directory. And we provided a few tools to get you started right away.

## Getting started: a dmake tutorial

Suppose you want to build an architecture with 3 different Ubuntu containers. The first thing is to get them running with Docker, as you'd do with your usual containers anyway.

Then we provide a few shortcuts to convert this machines into your docker-compose files. The rest is copy/paste. Easy.

For example, let's create a project and run 3 containers that just wait forever::

```text
$ mkdir sandbox # Or you can start from an existing git repository
$ cd sandbox
$ docker run --name my_container1 ubuntu sleep infinity &
$ docker run --name my_container1 ubuntu sleep infinity &
$ docker run --name my_container1 ubuntu sleep infinity &
```

You've got an Ubuntu container running and waiting forever. Let's integrate it into our project.

```text
$ dmake config
```

We've now created a `provision` directory with all the necessary files to have your architecture up and ready. You just have to start it right away:

```text
$ dmake stack start
```

=&gt; Et voilà. Your stack is up and running again.

From there you can make changes to your existing containers and if you want to update your containers according to the current configuration, just execute again:

```text
$ dmake config
$ dmake stack stop
$ dmake stack start # (should implement dmake stack restart, sorry)
```

Then, from your project's root:

```text
$ dmake

$ dmake -h

$ dmake status -h   # From an in-depth review of how your files should be layed out.
```

## TODO

* Integrate Kubernetes instead of Swarm

## FAQ

## Testing dmake

Use a virtualenv, pretty please. The rest is pretty easy:

$ pip install -e . $ pip install pytest $ python -m pytest \[--skipslow\]

or

$ make test


## Release dmake

(useful for internal folks)

$ make
$ make release
$ make dist

Username is 'ncube'
Password is in the vault ;)


