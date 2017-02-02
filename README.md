<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Read Me</title>

    <style type="text/css">
        .usage{
            margin-top: 30px;
            margin-left: 15px;
            word-spacing: 10px;
        }
        .opt th{
            text-align: left;
            width: 50%;
        }
        .dis{
                hanging-punctuation: first;
                font-weight: bold;
                border: 10px red;
        }


    </style>

</head>
<body>

<h3>Myip</h3>

<h5>Simple script for getting your wan ip address or info for an ip address or
    domain, using ipinfo api or via dns</h5>

<div class="dis">
    <h3>Disclaimer:</h3>
    <p>
        This script uses ipinfo api, which can be used for free up to 1000 queries a day.
    </p>
    <p>
        For more information go to <a href="http://ipinfo.io/developers/terms-of-use">ipinfo terms of use</a>.
    </p>
</div>

<p>Demo avaiable at <a href="https://asciinema.org/a/9jmu3058rtzvtwhf6ql8twk2n">asciinema</a> .</p>

<div class="usage">
    <p>usage: myip.py [-h] [-c] [-l] [-i IP [IP ...]] [-o OUTPUT] [-g] [-f FILE]</p>
</div>

<div class="opt">
    <table>
        <caption>optional arguments:</caption>
        <tr>
            <th>Argument</th>
            <th>Usage</th>
        </tr>
        <tr>
            <td>-h, --help</td>
            <td>show this help message and exit</td>
        </tr>
        <tr>
            <td>-c, --copy</td>
            <td>copy ip address to clipboard</td>
        </tr>
        <tr>
            <td>-l, --location</td>
            <td>Show location information</td>
        </tr>
        <tr>
            <td>-i IP [IP ...], --ip IP [IP ...]</td>
            <td>Provide ip address instead</td>
        </tr>
        <tr>
            <td>-o OUTPUT, --output OUTPUT</td>
            <td>Output results to a file</td>
        </tr>
        <tr>
            <td>g, --gmap</td>
            <td>Get google maps link</td>
        </tr>
        <tr>
            <td>-f FILE, --file FILE</td>
            <td>Read list of ip addresses from file</td>
        </tr>
    </table>
</div>
</body>

</html>
