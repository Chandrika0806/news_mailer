from flask import Flask, render_template, request, redirect, url_for, session
from functions import load_users, save_users, fetch_news, send_email
