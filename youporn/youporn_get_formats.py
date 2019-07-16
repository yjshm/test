#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import sys
import youtube_dl

ydl_sd_url = ""
ydl_hd_url = ""
ydl_opts = {'proxy':'192.168.1.106:1080'}
ydl_video_id = sys.argv[1]
#ydl_video_url = 'https://www.youtube.com/watch?v=' + ydl_video_id
ydl_video_url = 'https://www.youporn.com/watch/'+ ydl_video_id
#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
with youtube_dl.YoutubeDL() as ydl:
	video = ydl.extract_info(ydl_video_url, download=False)

formats = video.get('formats')

file_count = len(formats)
#print(formats)
for f in formats:
	format_id = f.get('format_id')
	#if 1 == format_id:
	if format_id.find('480p')>=0:
		ydl_sd_url = f.get('url')
	elif format_id.find('720p')>=0:
		ydl_hd_url = f.get('url')

if ydl_sd_url =="" and ydl_hd_url=="":
	for f in formats:
		format_id = f.get('format_id')
		#if 1 == format_id:
		if format_id.find('1')>=0:
			ydl_sd_url = f.get('url')
		elif format_id.find('3')>=0:
			ydl_hd_url = f.get('url')



print('[OVT]')
print(ydl_sd_url) 
print(ydl_hd_url)
