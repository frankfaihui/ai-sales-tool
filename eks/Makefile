build-ai-sales-api:
	cd ../ai-sales-api && docker build . -t ai-sales-api

build-ai-sales-web:
	cd ../ai-sales-web && docker build . -t ai-sales-web

push-ai-sales-api:
	docker tag ai-sales-api:latest 874128104192.dkr.ecr.us-west-2.amazonaws.com/ai-sales-tool:ai-sales-api
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 874128104192.dkr.ecr.us-west-2.amazonaws.com
	docker push 874128104192.dkr.ecr.us-west-2.amazonaws.com/ai-sales-tool:ai-sales-api

push-ai-sales-web:
	docker tag ai-sales-web:latest 874128104192.dkr.ecr.us-west-2.amazonaws.com/ai-sales-tool:ai-sales-web
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 874128104192.dkr.ecr.us-west-2.amazonaws.com
	docker push 874128104192.dkr.ecr.us-west-2.amazonaws.com/ai-sales-tool:ai-sales-web


