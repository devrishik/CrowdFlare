import boto.mturk.connection

from django.conf import settings

from .models import HIT

 
mturk = boto.mturk.connection.MTurkConnection(
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
    host = settings.MTURK_URL,
    debug = 1 # debug = 2 prints out all requests.
)

url = "https://crowdflare.ngrok.io/turk"
title = "News or not"
description = "Given a url, find if its a news website or not"
keywords = ["news", "research study", "penn state"]
frame_height = 500 # the height of the iframe holding the external hit
amount = 1
 
questionform = boto.mturk.question.ExternalQuestion( url, frame_height )

def create_hit():
	create_hit_result = mturk.create_hit(
	    title = title,
	    description = description,
	    keywords = keywords,
	    question = questionform,
	    reward = boto.mturk.price.Price( amount = amount),
	    response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
	)

	# return create_hit_result

	hit = create_hit_result[0]

	return HIT.objects.create(
		hit_id=hit.HITId,
		url=url,
		title=title,
		keywords=keywords,
		description=description,
		frame_height=frame_height,
		amount=amount)


def create_good_hit():
	hit = create_hit()
	hit.expected_bias = HIT.GOOD
	hit.save()
	return hit

def create_malicious_hit():
	hit = create_hit()
	hit.expected_bias = HIT.MALICIOUS
	hit.save()
	return hit

def create_random_hit():
	return create_hit()
