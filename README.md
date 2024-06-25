# Hydra Github UMB Bridge

## Background

The existing [hydra service](https://spaces.redhat.com/pages/viewpage.action?pageId=210863312) enables a user to configure github webhooks. Once configured, GitHub will start sending github events payload to the bridge endpoint, and upon successful cryptographic verification of the payload, the hydra bridge service publishes the webhooks events to UMB.

## Problem Statement

While the hydra webhook configuration makes the github events payload accessible within the Red Hat firewall, it has two major drawbacks:

- **Static Payloads**: The payloads sent by GitHub webhooks adhere to a [predefined templates](https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28) and are automatically generated based on the event that occurred. Users are unable to customize these payloads.
  
- **Event-Driven Architecture**: GitHub webhooks are designed to trigger on predefined events (e.g., push, pull request, issue comments). They cannot be triggered on-demand for arbitrary or custom evenst, as and when intended by users.

As a user, I should be able to publish a custom payload on-demand. This feature provides greater flexibility by allowing tailored data communication. Additionally, enabling on-demand publishing would limit the number of events being published, as it allows users to first process and filter messages, ensuring only relevant events are published.

## Solution

The [Hydra REST API Code](https://gitlab.cee.redhat.com/Workflow_Integration/hydra-sp/umb-bridge/-/blob/master/src/main/java/com/redhat/hydra/rest/BridgeRest.java?ref_type=heads#L39) accepts a JSON payload, and forwards it to the [bridge service](https://gitlab.cee.redhat.com/Workflow_Integration/hydra-sp/umb-bridge/-/blob/master/src/main/java/com/redhat/hydra/service/BridgeService.java). Upon successful verification of the signature, the bridge service publishes the payload to a UMB topic.

This project utilizes the existing Hydra bridge service to send a custom payload to the UMB topic by replicating the API call with the necessary payload properties and header values. The UMB topic in which the message will get published is [determined](https://gitlab.cee.redhat.com/Workflow_Integration/hydra-sp/umb-bridge/-/blob/master/src/main/java/com/redhat/hydra/service/BridgeService.java#L152) by the value of `repository.full_name` in the payload. The hash signature is an HMAC hex digest which is generated using the webhook's secret token and the payload contents, and is sent using the `X-Hub-Signature-256` header value. The service uses this value to [validate the webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries#validating-webhook-deliveries)

## References

- [Validating Github Webhook Deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
- [Github Events Payload](https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28)
