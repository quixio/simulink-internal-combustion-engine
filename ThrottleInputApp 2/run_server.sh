#!/bin/sh
echo "${bearer_token}" > /usr/share/nginx/html/bearer_token
echo "${Quix__Workspace__Id}" > /usr/share/nginx/html/workspace_id
echo "${Quix__Portal__Api}" > /usr/share/nginx/html/portal_api
echo "${topic}" > /usr/share/nginx/html/topic
nginx -g "daemon off;"