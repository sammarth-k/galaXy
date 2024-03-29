# header
def head(galaxy):
    html = f"""<html> <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="./css/style.css" rel="stylesheet"> <meta name="author" content="Sammarth Kumar"> <link rel="shortcut icon" type="image/x-icon" href="./images/logo.svg"/> <title>{galaxy} Data Access System</title> </head> <body onload="myfunc()"> <div id="loader" class="visible"> <img alt="Image" alt="load" src="./images/logo.svg"> </div><div id="searchbar"> <button id="search" onclick="search()">🔍</button> <div id="field"> <input id="searchfield" type="text" placeholder="Enter source coordinates"> <button onclick="searchbar(document.getElementById('searchfield').value)">Submit</button> <button onclick="document.getElementById('searchfield').value='';">Clear</button> <div id="displayres"></div></div></div><header name="header"> <br><br><br><br><h1 align="center">{galaxy} Data Access System</h1> <br><br><br><br>"""
    return html


# top of table
def table_top(binnings):
    html = f"""<table align="center"> <tr id="head"> <th> &check; </th> <th> S.No.</th><th>Source</th><th>ObsID</th><th>Total Counts</th><th>Observation Time(ks)</th><th>Count Rate(ks)</th><th>Cumulative Plot</th>"""
    for binning in binnings:
        html += f"""<th>Lightcurve ({binning}s)</th>"""
    html += """</tr>"""
    return html


# rows
def table_row(dict, count, binnings):
    html = f"""<tr id='{count}'><td><input type="checkbox" class="input" onchange="h({count},this)"></td><td>{count}</td><td>{dict['Source']}</td><td>{dict['ObsID']}</td><td>{dict['Counts']}</td><td>{round(dict['Obs. Time'],2)}</td><td>{round(dict['Count Rate'],2)}</td><td><a href="./images/cumulatives/cumulative_{count}.png" target="_blank">Cumulative</a></td>"""
    for binning in binnings:
        html += f"""<td><a href="./images/lightcurves/{binning}/lightcurve_{count}.png" target="_blank">{binning}</a></td>"""

    return html


# bottom part of file
def table_bottom():
    html = """
    </table><br><br><br><br></body><footer id="footer">Developed and Designed by Sammarth Kumar. Created with <span class="h">&#10084;</span> for the astro community </footer></html> <script src="./js/script.js"></script>
    """
    return html


# css code
def css():
    css = "html{scroll-behavior:smooth;font-family:sans-serif}body{margin:2px;background:#2c2c2c;color:#f5f5f5}#loader{z-index:2;position:fixed;width:100%;height:100%;background:#2c2c2c;color:#f5f5f5;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;vertical-align:middle}#loader img{margin:auto}a{color:#ff417a;text-decoration:none;-webkit-transition:.8s color;-o-transition:.8s color;transition:.8s color}a:hover{color:#f5f5f5}table{border:2px solid #ff417a;text-align:center;padding:0}td{padding:.4rem}td:not(:last-child){border-right:1px solid #f5f5f5}tr{border-bottom:1px solid #f5f5f5;-webkit-transition:1s background;-o-transition:1s background;transition:1s background}th{padding:1rem}#head{background:#ff417a}#search{font-size:1.5rem;cursor:pointer;z-index:1;position:fixed;top:0}#field{margin:auto;position:fixed;z-index:1;top:3rem;padding:1rem;border:2px solid #ff417a;border-radius:5px;-webkit-transform:translateX(-30rem);-ms-transform:translateX(-30rem);transform:translateX(-30rem);background:#2c2c2cee;-webkit-transition:1s -webkit-transform;transition:1s -webkit-transform;-o-transition:1s transform;transition:1s transform;transition:1s transform,1s -webkit-transform}#field input{border:1px solid #ff417a;padding:.2rem;color:#f5f5f5;background:#2c2c2c;border-radius:5px;font-size:1rem;margin-bottom:.2rem}#field #displayres{padding-top:2px}button{border:none;padding:.3rem .4rem;font-size:1rem;border-radius:5px;background:#ff417a;color:#f5f5f5;text-align:center;margin:.1rem}footer{background:#2c2c2c;z-index:1;position:fixed;bottom:0;text-align:center;width:100%;padding:8px 16px}.h{color:#ff417a}"
    return css


# javascript code
def js(ob):
    js = (
        "tosearch="
        + ob
        + """;function searchbar(obj){src=obj; for (let e=0; e < tosearch.length; e++){const t=tosearch[e]; if(t['Source'].includes(src)){document.getElementById("displayres").innerHTML="<a href='#" + String(e + 1) + "'>" + t.Source + "</a>";}}}function myfunc(){document.getElementById("loader").style.display="none"; if (localStorage.getItem("marked")==undefined){localStorage.setItem("marked", "");}else{if (localStorage.getItem("marked") !==""){array=localStorage.getItem("marked"); array=array.split(","); for (let index=0; index < array.length; index++){const element=parseInt(array[index]); document.getElementsByClassName("input")[element - 1].checked=true; document.getElementById(element).style.backgroundColor="#FF417Aaa";}}}}function h(ob, box){if (box.checked==false){document.getElementById(ob).style.background="none"; array=localStorage.getItem("marked"); array=array.split(","); if (array.length==1){array=[];}else{console.log(array); array=array.splice(array.indexOf(ob) - 1, 1);}array=array.toString(); localStorage.setItem("marked", array);}else{document.getElementById(ob).style.background="#FF417Aaa"; array=localStorage.getItem("marked"); array=array.split(","); array.push([ob]); if (array[0]===""){array.shift();}array=array.toString(); localStorage.setItem("marked", array);}}function search(){if (document.getElementById("field").style.transform=="translateX(0rem)"){document.getElementById("field").style.transform="translateX(-30rem)";}else{document.getElementById("field").style.transform="translateX(0rem)";}}"""
    )
    return js


# logo svg code
def logo():
    logo = """<svg width="500" height="500" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="500" height="500" fill="#2C2C2C"/><path d="M100.352 216.281V223.306L92.4206 225.346C93.871 227.612 94.5962 230.15 94.5962 232.961C94.5962 238.399 92.6926 242.645 88.8853 245.697C85.1083 248.718 79.8507 250.229 73.1125 250.229L70.6197 250.093L68.5801 249.866C67.1599 250.954 66.4498 252.163 66.4498 253.492C66.4498 255.487 68.988 256.484 74.0643 256.484H82.6759C88.2357 256.484 92.466 257.677 95.3667 260.064C98.2977 262.451 99.7632 265.957 99.7632 270.58C99.7632 276.502 97.2854 281.095 92.33 284.358C87.4048 287.622 80.3191 289.253 71.0729 289.253C64.0023 289.253 58.5936 288.014 54.8468 285.537C51.1302 283.089 49.2719 279.644 49.2719 275.203C49.2719 272.151 50.2238 269.598 52.1274 267.543C54.031 265.488 56.826 264.023 60.5124 263.146C59.0922 262.542 57.8533 261.56 56.7958 260.2C55.7382 258.81 55.2094 257.345 55.2094 255.804C55.2094 253.87 55.7684 252.269 56.8864 251C58.0044 249.7 59.621 248.431 61.7361 247.192C59.0771 246.044 56.962 244.201 55.3907 241.663C53.8497 239.125 53.0792 236.133 53.0792 232.689C53.0792 227.159 54.877 222.883 58.4728 219.862C62.0685 216.84 67.2052 215.329 73.883 215.329C75.3032 215.329 76.9802 215.465 78.914 215.737C80.8781 215.979 82.132 216.16 82.6759 216.281H100.352ZM61.2375 274.115C61.2375 276.019 62.144 277.514 63.957 278.602C65.8002 279.69 68.3686 280.234 71.6621 280.234C76.6176 280.234 80.5004 279.554 83.3105 278.194C86.1206 276.834 87.5256 274.976 87.5256 272.619C87.5256 270.716 86.6947 269.401 85.0328 268.676C83.3709 267.951 80.8025 267.588 77.3277 267.588H70.1664C67.6283 267.588 65.498 268.177 63.7757 269.356C62.0836 270.565 61.2375 272.151 61.2375 274.115ZM66.2685 232.87C66.2685 235.62 66.888 237.795 68.1268 239.397C69.3959 240.998 71.3146 241.799 73.883 241.799C76.4816 241.799 78.3852 240.998 79.5939 239.397C80.8025 237.795 81.4068 235.62 81.4068 232.87C81.4068 226.766 78.8989 223.714 73.883 223.714C68.8067 223.714 66.2685 226.766 66.2685 232.87ZM140.918 266.954L138.243 260.064H137.881C135.554 262.995 133.152 265.035 130.674 266.183C128.227 267.301 125.024 267.86 121.066 267.86C116.201 267.86 112.363 266.47 109.553 263.69C106.773 260.91 105.383 256.952 105.383 251.815C105.383 246.437 107.257 242.479 111.004 239.94C114.781 237.372 120.461 235.952 128.046 235.68L136.838 235.408V233.187C136.838 228.05 134.21 225.482 128.952 225.482C124.903 225.482 120.144 226.706 114.675 229.153L110.097 219.816C115.929 216.765 122.395 215.239 129.496 215.239C136.295 215.239 141.507 216.719 145.133 219.681C148.759 222.642 150.572 227.144 150.572 233.187V266.954H140.918ZM136.838 243.476L131.49 243.657C127.471 243.778 124.48 244.503 122.516 245.833C120.552 247.162 119.57 249.187 119.57 251.906C119.57 255.804 121.806 257.753 126.278 257.753C129.481 257.753 132.034 256.831 133.938 254.988C135.871 253.145 136.838 250.697 136.838 247.646V243.476ZM178.673 266.954H164.849V196.429H178.673V266.954ZM225.402 266.954L222.728 260.064H222.365C220.039 262.995 217.636 265.035 215.159 266.183C212.711 267.301 209.508 267.86 205.55 267.86C200.685 267.86 196.848 266.47 194.038 263.69C191.258 260.91 189.868 256.952 189.868 251.815C189.868 246.437 191.741 242.479 195.488 239.94C199.265 237.372 204.946 235.952 212.53 235.68L221.323 235.408V233.187C221.323 228.05 218.694 225.482 213.436 225.482C209.387 225.482 204.628 226.706 199.159 229.153L194.582 219.816C200.413 216.765 206.879 215.239 213.98 215.239C220.779 215.239 225.991 216.719 229.617 219.681C233.243 222.642 235.056 227.144 235.056 233.187V266.954H225.402ZM221.323 243.476L215.975 243.657C211.956 243.778 208.964 244.503 207 245.833C205.036 247.162 204.054 249.187 204.054 251.906C204.054 255.804 206.29 257.753 210.762 257.753C213.965 257.753 216.518 256.831 218.422 254.988C220.356 253.145 221.323 250.697 221.323 247.646V243.476ZM386.756 216.281H401.895L411.458 244.79C412.274 247.268 412.833 250.199 413.135 253.583H413.407C413.739 250.471 414.389 247.54 415.356 244.79L424.738 216.281H439.559L418.121 273.435C416.157 278.723 413.347 282.681 409.69 285.31C406.064 287.939 401.819 289.253 396.954 289.253C394.567 289.253 392.225 288.996 389.929 288.483V277.514C391.591 277.907 393.404 278.103 395.368 278.103C397.815 278.103 399.946 277.348 401.759 275.837C403.602 274.357 405.037 272.106 406.064 269.084L406.88 266.591L386.756 216.281Z" fill="#F5F5F5"/><path d="M408.535 340H359.676L312.749 263.675L265.823 340H220L286.94 235.933L224.279 138.215H271.481L314.958 210.814L357.606 138.215H403.704L340.353 238.28L408.535 340Z" fill="#FF417A"/></svg>"""
    return logo
