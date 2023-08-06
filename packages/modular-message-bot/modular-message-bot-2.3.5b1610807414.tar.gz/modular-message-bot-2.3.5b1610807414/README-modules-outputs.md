# Output Modules

## Specifics

### Standard Out Output Module
This one is great for testing

Example Output:
```yaml
- code: stdout
  parameters:
    message: "Hello World! {some_string_here}"
```

### Slack Output Module
The slack module is very dynamic anything you add to the "payload" gets sent as json to the slack URL you specify
See: https://api.slack.com/messaging/webhooks

Example Output:
```yaml
- code: slack
  parameters:
    url: "$[SLACK_URL]"
    payload:
      text: "{msg}"
      channel: "#test"
      post-as: "$[SLACK_NAME]"
      icon_emoji: ":information_source:"
```

### Easy HTTP Output Module
This module is very flexible, it is used to push http(s) payloads. It is basically a wrapper around Python request.
Anything in the args is passed directly into `requests.request` as an argument (i.e. headers are optional).

Example Output:
```yaml
- code: easy_http
  parameters:
    url: "https://something.example.com/path/here"
    method: put
    ignore-failure: True
    args:
      headers:
        Auth-Token: "${TEST_AUTH_CODE}"
      json:
        message: "{msg}"
        duration: "30000"
```

### Pushover Output Module
Sends notifications to Pushover. This module is very similar to the docs (https://pushover.net/api)
Feature Maturity Status: Alpha
Note: We need to implement more features to be nicer to their API such as rate limiting the output. See:

Example Simple Output:
```yaml
- code: pushover
  parameters:
    token: "azGDORePK8gMaC0QOYAMyEEuzJnyUi"
    user: "uQiRzpo4DXghDmr9QzzfQu27cmVRsG"
    message: "Hello World!!!"
```

Example Advanced Output:
```yaml
- code: pushover
  parameters:
    token: "azGDORePK8gMaC0QOYAMyEEuzJnyUi"
    user: "uQiRzpo4DXghDmr9QzzfQu27cmVRsG"
    message: "Hello World!!!"
    device: droid2
    title: "Direct message from @someuser"
    url: "twitter://direct_message?screen_name=someuser"
    url_title: "Reply to @someuser"
    priority: "1"
    sound: incoming
    timestamp: "1331249662"
```
