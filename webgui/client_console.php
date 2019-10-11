
<!DOCTYPE html>
<html>
<head>
<title>SystemImager client install logs.</title>
  <style type='text/css' media='screen'>@import url('css/screen.css');</style>
  <style type='text/css' media='screen'>@import url('css/sliders.css');</style>
  <!-- <style type='text/css' media='screen'>@import url('css/print.css');</style> -->
  <script src="functions.js"></script>
</head>
<body>

<?php
if (isset($_GET["client"])) {
    $client=$_GET["client"];
} else {
    $client="error.json";
}
?>
<!-- SystemImager header -->
<table id="headerTable">
  <tbody>
    <tr>
      <td><img src="css/SystemImagerBanner.png" alt="SystemImagezr"></td>
      <td id="clientData1">&nbsp;</td>
      <td id="clientData2">&nbsp;</td>
    </tr>
  </tbody>
</table>
<p>
<hr>
<table id="filtersTable" width="99%">
  <tbody>
    <tr id="filtersRow">
      <td>Filters:
        <span class='pri_debug'>Debug</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'debug')" checked>
          <span class="slider round"></span>
        </label>
        <span class='pri_system'>System</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'system')" checked>
          <span class="slider round"></span>
        </label>
        <span class='pri_notice'>Notice</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'notice')" checked>
          <span class="slider round"></span>
        </label>
        <span class='pri_detail'>Detail</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'detail')" checked>
          <span class="slider round"></span>
        </label>
        <span class='pri_stdout'>StdOut</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'stdout')" checked>
          <span class="slider round"></span>
        </label>
        <span class='pri_stderr'>StdErr</span>
        <label class="switch">
          <input type="checkbox" onclick="doFilter(this,'stderr')" checked>
          <span class="slider round"></span>
        </label>
      </td>
      <td style="text-align:right">
        <span>Refresh:</span>
        <label class="switch">
          <input type="checkbox" id="refresh_checkbox" onclick="doRefresh(this)" checked>
          <span class="slider round"></span>
        </label>
        <span id="refresh_text">No</span>
      </td>
    </tr>
  </tbody>
</table>
<hr>
<p>

<table id="logTable">
  <thead>
    <tr><th>Tag</th><th>Priority</th><th>Message</th></tr>
  </thead>
  <tbody id="serverData">
  </tbody>
</table>

<script type="text/javascript">
var eSource; // Global variable.

//check for browser support
if (!!window.EventSource) {
  EnableRefresh();
} else {
  document.getElementById("filtersRow").innerHTML="<td>Whoops! Your browser doesn't receive server-sent events.<br>Please use a web browser that supports EventSource interface <A href='https://caniuse.com/#feat=eventsource'>https://caniuse.com/#feat=eventsource</A></td>";
  document.getElementById("logTable").style.display="none";
  // sleep(5); // BUG: sleep does not exists.
  // Fallback: redirect to static page with refresh.
  // do an eSource.close(); when client has disconnected.
}

// Log connection established
eSource.addEventListener('open', function(e) {
  console.log("Connection was opened.")
}, false);

// Log connection closed
eSource.addEventListener('error', function(e) {
  if (e.readyState == EventSource.CLOSED) { 
    console.log("Connection was closed. ");
  }
}, false);


function EnableRefresh() {
  eSource=new EventSource('push_client_logs.php?client=<?php echo $client; ?>');  //instantiate the Event source
  // eSource.addEventListener('message', UpdateLogHandler, false);
  eSource.addEventListener('resetlog', ResetLogHandler, false); // resetlog: when log has changed (reinstall)
  eSource.addEventListener('updatelog', UpdateLogHandler, false); // New lines in log
  eSource.addEventListener('updateclient', UpdateClientHandler , false); // client updated status or progress.
  document.getElementById("refresh_text").innerHTML="Active";
  refresh_span=document.getElementById("refresh_text");
  refresh_span.innerHTML="Yes";
  refresh_span.setAttribute("class","pri_info");
}

function DisableRefresh() {
  eSource.removeEventListener('updateclient', UpdateClientHandler , false);
  eSource.removeEventListener('updatelog', UpdateLogHandler, false);
  eSource.removeEventListener('resetlog', ResetLogHandler, false);
  eSource.close();
  refresh_span=document.getElementById("refresh_text");
  refresh_span.innerHTML="No";
  refresh_span.setAttribute("class","pri_stderr");
}

function doRefresh(checkBox) {
    if (checkBox.checked == true) {
        EnableRefresh();
    } else {
        DisableRefresh();
    }
}

// Clean log if requested (in case of reimage for example)
function ResetLogHandler(event) {
  document.getElementById("serverData").innerHTML=""; // Remove all table lines.
}

// Called when event updatelog is received
function UpdateLogHandler(event) {
  var logText;
  try { 
    var logInfo = JSON.parse(event.data);
    logLine = LogToHTML(logInfo.TAG,logInfo.PRIORITY,logInfo.MESSAGE);
  } catch (e) {
    console.error("JSON client_log parsing error: ", e);
    // console.error("JSON: ", event.data);
    logLine = LogToHTML('webgui','local0.err',event.data); // BUG: invalid chars may appear and is subject to injection.
  }
// Stack overflow question:
// https://stackoverflow.com/questions/58014912/how-can-scroll-down-a-tbody-table-when-innerhtml-is-updated-with-new-lines
  // console.log("log: " . logInfo.type . ": " . logInfo.message);
  // var logText = "log: " + logInfo.TAG + " - " + logInfo.PRIORITY + ": " + logInfo.MESSAGE + "<br>";
  document.getElementById("serverData").innerHTML += logLine;
}

function LogToHTML(tag,value,message) { // Original values from systemimager-lib.sh:logmessage()
    switch(value) {
        case 'local2.info': // stdout
            return "<tr class='filter_stdout'><td>"+tag+"</td><td><span class='pri_stdout'>StdOut</span></td><td>"+message+"</td></tr>";
            break;
        case 'local2.err': // stderr
            return "<tr class='filter_stderr'><td>"+tag+"</td><td><span class='pri_stderr'>StdErr</span></td><td>"+message+"</td></tr>";
            break;
        case 'local2.notice': // kernel info
            return "<tr class='filter_system'><td>"+tag+"</td><td><span class='pri_system'>Kernel</span></td><td>"+message+"</td></tr>";
            break;
        case 'local1.debug': // log STEP
            return "<tr class='filter_debug'><td>"+tag+"</td><td><span class='pri_debug'>===STEP</span></td><td>"+message+"</td></tr>";
            break;
        case 'local1.info': // detail
            return "<tr class='filter_detail'><td>"+tag+"</td><td><span class='pri_detail'>Detail</span></td><td>"+message+"</td></tr>";
            break;
        case 'local1.notice': // notice
            return "<tr class='filter_notice'><td>"+tag+"</td><td><span class='pri_notice'>Notice</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.info': // info
            return "<tr><td>"+tag+"</td><td><span class='pri_info'>Info</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.warning': // warning
            return "<tr><td>"+tag+"</td><td><span class='pri_warning'>Warning</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.err': // ERROR
            return "<tr><td>"+tag+"</td><td><span class='pri_error'>ERROR</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.notice': // action
            return "<tr><td>"+tag+"</td><td><span class='pri_action'>Action</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.debug': // debug
            return "<tr class='filter_debug'><td>"+tag+"</td><td><span class='pri_debug'>Debug</span></td><td>"+message+"</td></tr>";
            break;
        case 'local0.emerg': // FATAL
            return "<tr><td>"+tag+"</td><td><span class='pri_fatal'>FATAL</span></td><td>"+message+"</td></tr>";
            break;
        default: // All other messages are system messages (not systemimager)
            return "<tr class='filter_system'><td>"+tag+"</td><td><span class='pri_system'>System</span></td><td>"+message+"</td></tr>";
            break;
    } 
}

// Called when event updateclient is received
function UpdateClientHandler(event) {
  try {
    var clientInfo = JSON.parse(event.data);
    var clientText1 = "Hostname: " + clientInfo.host + 
                      "<br>MAC: " + clientInfo.name +
                      "<br>IP: " + clientInfo.ip +
                      "<br>Image: " + clientInfo.os +
                      "<br>Status: " + StatusToText(clientInfo.status);
//                      "<br>" + get_status(clientInfo.status);

    var clientText2 = "CPU(s): " + clientInfo.ncpus + " x " + clientInfo.cpu +
                      "<br>Memory: " + Math.trunc(clientInfo.mem / 1024) +
                      " MiB<br>Kernel: " + clientInfo.kernel +
                      "<br>Started: " + UnixDate(clientInfo.first_timestamp) +
                      "<br>Duration: " + (clientInfo.timestamp - clientInfo.first_timestamp) +'s';
    document.getElementById("clientData1").innerHTML = clientText1;
    document.getElementById("clientData2").innerHTML = clientText2;
  } catch (e) {
    console.error("JSON client_info parsing error: ", e);
    // console.error("JSON: ", event.data);
  }
}

function doFilter(checkBox, msg_type) {
    var display;
    if (checkBox.checked == true) {
        display = "block";
    } else {
        display = "none";
    }

    var myClasses = document.querySelectorAll('.filter_'+msg_type),
    i = 0,
    l = myClasses.length;

    for (i; i < l; i++) {
        myClasses[i].style.display = display;
    }
}

</script>

</body>
</html>
