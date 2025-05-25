#!/bin/bash

watchfiles "celery -A celery_tasks worker -l INFO"