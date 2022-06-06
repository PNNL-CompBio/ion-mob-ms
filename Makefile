push-all-images:
	# pushing the locally built docker images from dockerfiles at ./docker/ to https://hub.docker.com/anubhav0fnu.
	@docker push anubhav0fnu/mzmine:latest
	@docker push anubhav0fnu/autoccs:latest
	@docker push anubhav0fnu/ccs_comparison:latest
	@docker push anubhav0fnu/pnnl_preprocessor:latest

build-images:
	# building the docker images from dockerfiles
	@docker build -t anubhav0fnu/autoccs:latest -f docker/autoccs ./docker/
	@docker build -t anubhav0fnu/ccs_comparison:latest -f docker/ccs_comparison ./docker/
	@docker build -t anubhav0fnu/mzmine:latest -f docker/mzmine ./docker/
	@docker build -t anubhav0fnu/pnnl_preprocessor:latest -f docker/pnnl_preprocessor ./docker/

pull-images:
	# pulling dockerimages from dockerhub
	@docker pull proteowizard/pwiz-skyline-i-agree-to-the-vendor-licenses:latest
	@docker pull r-base:latest
	@docker pull anubhav0fnu/proteowizard:latest
	@docker pull anubhav0fnu/ccs_comparison:latest
	@docker pull anubhav0fnu/pnnl_preprocessor:latest
	@docker pull anubhav0fnu/mzmine:latest
	@docker pull anubhav0fnu/autoccs:latest

