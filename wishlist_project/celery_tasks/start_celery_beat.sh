#!/bin/bash

watchfiles "celery -A celery_tasks beat -l INFO"