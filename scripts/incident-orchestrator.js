// scripts/incident-orchestrator.js
if (incident.type === 'secret' && incident.validity === 'valid') {
await createJiraTicket(incident);
await triggerPagerDuty(incident.severity);
await autoRotateAndCommentPR(incident);
}
