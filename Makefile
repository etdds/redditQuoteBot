NAME   := etdds/reddit-quote-bot
TAG    := $$(git log -1 --pretty=%h)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

run-image:
	@docker run --rm -v $(PWD):/home/app_user/run ${LATEST}

build-image:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

test:
	@python -m unittest discover -v -s ./tests -p test_*.py 

clean:
	@rm -rf *.egg-info
	@rm -rf build
	@rm -rf dist
	@rm -rf .eggs
