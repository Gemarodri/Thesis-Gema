#!/bin/bash

chromium-browser https://github.com/elastic/elasticsearch/blame/$1/$2 > /dev/null 2>&1 &

