REPO = "kianjones9/blog"
tag = "latest"

build: ;docker build -t ${REPO}:${tag} .

.PHONY: build

push: ;docker push ${REPO}:${tag}
