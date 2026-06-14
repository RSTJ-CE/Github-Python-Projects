channelID =  3229434;
ReadApiKey ='...';
writeApiKey = '...';

%Set up email
setpref('Internet','E_mail',''); %enter email
setpref('Internet','SMTP_Server','smtp.gmail.com');
setpref('Internet','SMTP_Username','...'); %enter email
setpref('Internet','SMTP_Password','...'); %enter email app passcode


props = java.lang.System.getProperties; %get java system settings
props.setProperty('mail.smtp.auth','true'); %login to email
props.setProperty('mail.smtp.socketFactory.class','javax.net.ssl.SSLSocketFactory'); %use secure SSL connection
props.setProperty('mail.smtp.socketFactory.port','465'); %use gmail port 465


%Subject of email
alertSubject = sprintf("Mobile Flood Detector");


% Read the recent data.
FloodData = thingSpeakRead(channelID,'NumPoints',2,'Fields',1,'ReadKey',ReadApiKey); % 2 points from Flood data
DrainBlockageData = thingSpeakRead(channelID,'NumPoints',1,'Fields',2,'ReadKey',ReadApiKey); % 1 point from Drain blockage data
alertBody = '';
flood_threshold = 4;
send_email = false;

%For flood data
if isempty(FloodData) %there is no flood data
    Current_value = 0;
    Previous_value = 0;
elseif length(FloodData) == 1 %there is 1 flood data
    Current_value = FloodData(end);
    Previous_value = 0;
else %More than 1 flood data
    Current_value = FloodData(end);
    Previous_value = FloodData(end-1);
end

%For drain blockage data
if isempty(DrainBlockageData)
    DrainBlockage_value = 0;
else
    DrainBlockage_value = DrainBlockageData(end);
end

%Conditions for sending email
if (DrainBlockage_value == 1) %No rain, drainblockage has a value
    send_email = true;
    alertBody = ["Drain blockage detected! Please inspect drainage system immediately."
                 "View live flood data at: https://thingspeak.com/channels/3229434"];
elseif (Current_value < flood_threshold) && ~(Previous_value < flood_threshold) %when flood has been resolved
    send_email = true;
    alertBody = ["Flood has been resolved! Monitoring will continue."
                 "View live flood data at: https://thingspeak.com/channels/3229434"];
elseif (Current_value >= flood_threshold) %Flood is occuring
    if (Previous_value < flood_threshold) %Flood just started
        send_email = true;
        alertBody = ["Flood detected! Please take immediate actions."
                     "View live flood data at: https://thingspeak.com/channels/3229434"];
    end
end

 %Catch errors so the MATLAB code does not disable a TimeControl if it fails
if (send_email)
  try
      sendmail('...', alertSubject, alertBody); %Enter receiver's email
  catch someException
      fprintf("Failed to send email: %s\n", someException.message);
  end
end
