"""Render the profile README architecture diagrams with official AWS Architecture Icons."""
import os
import sys

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

import diagrams

RES = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def aws(path, label):
    return Custom(label, f"{RES}/aws/{path}.png")


def ext(path, label):
    return Custom(label, f"{RES}/{path}.png")


GRAPH = {
    "fontsize": "26", "fontname": "Helvetica-Bold", "fontcolor": "#232F3E",
    "bgcolor": "white", "pad": "0.5", "nodesep": "0.9", "ranksep": "0.9", "splines": "spline",
    "dpi": "110", "labelloc": "t",
}
NODE = {"fontsize": "13", "fontname": "Helvetica", "fontcolor": "#232F3E"}
EDGE = {"fontsize": "12", "fontname": "Helvetica-Bold", "color": "#545B64", "fontcolor": "#232F3E"}


def cluster(label, color="#147EBA", bg="#F2F8FC"):
    return Cluster(label, graph_attr={
        "fontsize": "15", "fontname": "Helvetica-Bold", "fontcolor": color,
        "style": "rounded,dashed", "pencolor": color, "bgcolor": bg, "margin": "18",
    })


FLOW = lambda label="": Edge(label=label, color="#232F3E", penwidth="1.6")
FINDING = lambda label="": Edge(label=label, color="#DD344C", style="dashed", fontcolor="#DD344C")
CONTROL = lambda label="": Edge(label=label, color="#7AA116", style="dashed", fontcolor="#5A7A10")
GOVERN = lambda label="": Edge(label=label, color="#8C4FFF", style="dashed", fontcolor="#6B3AC2")

ACCOUNT = ("#E7157B", "#FDF2F8")
VPC = ("#8C4FFF", "#F7F3FF")
SUBNET = ("#7AA116", "#F4F9EC")
SECURITY = ("#DD344C", "#FDF3F4")
NEUTRAL = ("#545B64", "#F7F7F7")


def diagram(title, name, direction="TB"):
    return Diagram(title, filename=os.path.join(OUT, name), show=False, direction=direction,
                   outformat="png", graph_attr=GRAPH, node_attr=NODE, edge_attr=EDGE)


# 0 · Reference architecture -------------------------------------------------
with diagram("Reference Architecture · cloud-native, event-driven on AWS", "00-reference-architecture", "LR"):
    users = aws("general/users", "Web + mobile clients")
    with cluster("Edge", *NEUTRAL):
        cf = aws("network/cloudfront", "CloudFront\n+ AWS WAF")
    apigw = aws("network/api-gateway", "API Gateway")
    cognito = aws("security/cognito", "Cognito\nOAuth2 / JWT")
    with cluster("Compute", *SUBNET):
        svc = aws("compute/fargate", "NestJS services\nECS Fargate")
        fn = aws("compute/lambda", "Lambda\nfunctions")
    with cluster("Data", *VPC):
        pg = aws("database/aurora", "Aurora PostgreSQL\n+ pgvector")
        cache = aws("database/elasticache", "ElastiCache\nValkey / Redis")
    with cluster("Events (outbox)", *ACCOUNT):
        bus = [aws("analytics/managed-streaming-for-kafka", "Kafka (MSK)"),
               aws("integration/eventbridge", "EventBridge"),
               aws("integration/simple-notification-service-sns", "SNS")]
    sqs = aws("integration/simple-queue-service-sqs", "SQS + DLQ")
    with cluster("Async workers", *SUBNET):
        wrk = aws("compute/lambda", "Workers\nLambda / BullMQ")
    with cluster("Storage + analytics", *VPC):
        ddb = aws("database/dynamodb", "DynamoDB")
        lake = aws("storage/simple-storage-service-s3", "S3 data lake")
        ch = aws("general/generic-database", "ClickHouse\nanalytics")
    with cluster("Observability", *NEUTRAL):
        obs = [aws("management/cloudwatch", "CloudWatch"), aws("devtools/x-ray", "X-Ray"),
               aws("management/amazon-managed-grafana", "Grafana")]

    users >> FLOW() >> cf >> FLOW() >> apigw
    apigw >> Edge(style="dashed", label="authorise") >> cognito
    apigw >> FLOW() >> [svc, fn]
    svc >> FLOW() >> [pg, cache]
    svc >> FLOW("publish") >> bus[0]
    bus >> FLOW() >> sqs >> FLOW() >> wrk >> FLOW() >> [ddb, lake]
    lake >> FLOW() >> ch
    svc >> Edge(style="dotted", color="#879196", label="metrics + traces") >> obs[0]
    obs[0] >> Edge(style="invis") >> obs[1] >> Edge(style="invis") >> obs[2]


# 1 · Secure CI/CD pipeline --------------------------------------------------
with diagram("1 · Secure CI/CD pipeline: pull request → production", "01-devsecops-pipeline"):
    with cluster("SOURCE", *NEUTRAL):
        dev = aws("general/user", "Developer\nopens a PR")
        gh = ext("onprem/vcs/github", "① GitHub\nbranch protection\nsigned commits")
        with cluster("② PR checks · before merge", *SECURITY):
            pr_insp = aws("security/inspector", "Inspector\ncode security")
            pr_q = aws("ml/q", "Amazon Q\ncode review")
    conn = aws("devtools/codestar", "③ CodeConnections\nno stored keys")
    cp = aws("devtools/codepipeline", "CodePipeline V2")

    with cluster("④ BUILD GATES · CodeBuild in parallel · any failure stops the release", *ACCOUNT):
        g_secret = aws("devtools/codebuild", "Secrets scan\ngitleaks")
        g_sast = aws("security/inspector", "SAST + SCA\nInspector · Semgrep")
        g_iac = ext("onprem/iac/terraform", "IaC scan\nCheckov on plan")
        g_iam = aws("security/identity-and-access-management-iam-access-analyzer", "IAM policy check\nAccess Analyzer")
        g_test = aws("devtools/codebuild", "Unit + contract\ntests")
    gates = [g_secret, g_sast, g_iac, g_iam, g_test]

    with cluster("SUPPLY CHAIN", *VPC):
        img = ext("onprem/container/docker", "⑤ Build image + SBOM\ndistroless · non-root")
        ecr = aws("compute/ec2-container-registry", "⑥ Amazon ECR\nInspector scan\nblock on CRITICAL")
        sign = aws("security/security-identity-and-compliance", "⑦ AWS Signer\nsign image (Notation)")

    with cluster("STAGING ACCOUNT", *SUBNET):
        tf = ext("onprem/iac/terraform", "⑧ Terraform apply")
        stg = aws("compute/fargate", "ECS Fargate\nstaging")
        dast = aws("devtools/codebuild", "⑨ DAST · ZAP\n+ integration tests")

    with cluster("PRODUCTION ACCOUNT", *ACCOUNT):
        appr = aws("general/user", "⑩ Manual approval\nchange record")
        prod = aws("compute/elastic-container-service", "⑪ Verify signature →\nECS blue/green deploy")
        alarm = aws("management/cloudwatch-alarm", "CloudWatch alarms\nauto-rollback")

    with cluster("⑫ FINDINGS · one view for all scanners", *SECURITY):
        hub = aws("security/security-hub", "Security Hub")
        eb = aws("integration/eventbridge", "EventBridge")
        chat = ext("saas/chat/slack", "Slack / Teams\n+ Jira ticket")
        rep = aws("storage/simple-storage-service-s3", "Reports archive\nS3 Object Lock")

    dev >> FLOW() >> gh
    gh >> Edge(style="dashed", label="every PR") >> [pr_insp, pr_q]
    gh >> FLOW("merge to main") >> conn >> FLOW() >> cp >> FLOW() >> gates
    gates >> FLOW("all pass") >> img
    img >> FLOW("push") >> ecr >> FLOW() >> sign >> FLOW() >> tf >> FLOW() >> stg >> FLOW() >> dast
    dast >> FLOW() >> appr >> FLOW("approved") >> prod
    prod >> Edge(style="dashed", label="watches") >> alarm
    [pr_insp, g_sast, g_iac, ecr, dast] >> FINDING("findings") >> hub
    hub >> FLOW() >> eb >> FLOW() >> chat
    hub >> FLOW() >> rep


# 2 · Multi-account landing zone ---------------------------------------------
with diagram("2 · Multi-account landing zone and governance", "02-landing-zone"):
    idp = ext("saas/identity/okta", "Corporate IdP\nEntra ID / Okta")

    with cluster("① MANAGEMENT ACCOUNT · billing + organisation only, no workloads", *ACCOUNT):
        org = aws("management/organizations", "AWS Organizations")
        ct = aws("management/control-tower", "Control Tower\nlanding zone")
        sso = aws("security/single-sign-on", "② Identity Center\nMFA · temp roles")
        pol = aws("security/identity-and-access-management-iam-permissions",
                  "③ Guardrails\nSCPs · RCPs\ndeclarative policies")

    with cluster("SECURITY OU", *SECURITY):
        with cluster("④ Security Tooling account · delegated admin", *SECURITY):
            hub = aws("security/security-hub", "Security Hub")
            gd = aws("security/guardduty", "GuardDuty")
            insp = aws("security/inspector", "Inspector")
            macie = aws("security/macie", "Macie")
            det = aws("security/detective", "Detective")
            aa = aws("security/identity-and-access-management-iam-access-analyzer", "Access Analyzer")
        with cluster("⑤ Log Archive account · write-once", *SECURITY):
            trail = aws("management/cloudtrail", "Org CloudTrail")
            cfg = aws("management/config", "AWS Config")
            logs = aws("storage/simple-storage-service-s3", "S3 Object Lock")
            seclake = aws("security/security-lake", "Security Lake")

    with cluster("INFRASTRUCTURE OU", *VPC):
        with cluster("⑥ Network account", *VPC):
            tgw = aws("network/transit-gateway", "Transit Gateway")
            nfw = aws("network/network-firewall", "Network Firewall\ncentral egress")
            dnsfw = aws("network/route-53", "DNS Firewall")
        with cluster("⑦ CI/CD account", *VPC):
            pipe = aws("devtools/codepipeline", "CodePipeline")
            reg = aws("compute/ec2-container-registry", "ECR")

    with cluster("WORKLOADS OU · one account per environment", *SUBNET):
        dev = aws("management/organizations-account", "Dev")
        stg = aws("management/organizations-account", "Staging")
        prd = aws("management/organizations-account", "Production")
    with cluster("⑧ SANDBOX OU", *NEUTRAL):
        sbx = aws("management/organizations-account", "Sandbox\nbudget-capped")

    idp >> Edge(label="SAML + SCIM") >> sso
    org - ct
    pol >> GOVERN("applies to every account") >> stg
    pol >> GOVERN() >> [dev, prd, sbx]
    sso >> GOVERN("short-lived roles") >> prd
    pipe >> FLOW("deploy via per-account roles") >> stg
    pipe >> FLOW() >> [dev, prd]
    prd >> Edge(color="#879196", label="TGW attachment") >> tgw
    [dev, stg] >> Edge(color="#879196") >> tgw
    tgw - nfw
    stg >> FINDING("logs") >> trail
    stg >> FINDING("findings") >> hub
    [dev, prd] >> FINDING() >> trail
    [dev, prd] >> FINDING() >> hub
    trail >> Edge(style="dotted") >> logs
    trail >> Edge(style="dotted") >> seclake
    hub - gd


# 3 · Production runtime -----------------------------------------------------
with diagram("3 · Production runtime: defence in depth from edge to data", "03-production-runtime"):
    users = aws("general/users", "Users · apps\npartners")
    r53 = aws("network/route-53", "① Route 53\nDNSSEC · failover")
    with cluster("② EDGE", *NEUTRAL):
        cf = aws("network/cloudfront", "CloudFront\nTLS 1.3")
        waf = aws("security/waf", "AWS WAF\n+ Bot Control")
        shield = aws("security/shield-advanced", "Shield Advanced")

    with cluster("PRODUCTION VPC · 3 Availability Zones", *VPC):
        with cluster("④ PRIVATE APP SUBNETS", *SUBNET):
            alb = aws("network/elb-application-load-balancer", "Internal ALB\nno public IP")
            svc = aws("compute/fargate", "ECS Fargate\nnon-root · read-only")
            sqs = aws("integration/simple-queue-service-sqs", "SQS + DLQ")
            wrk = aws("compute/lambda", "Workers")
        with cluster("⑤ ISOLATED DATA SUBNETS · no internet route", *ACCOUNT):
            aur = aws("database/aurora", "Aurora PostgreSQL\nIAM auth · RLS")
            val = aws("database/elasticache", "ElastiCache\nValkey · TLS")
        vpce = aws("network/endpoint", "⑥ VPC endpoints\nPrivateLink")
        nfw = aws("network/network-firewall", "⑦ Network Firewall\nallow-list egress")

    s3ddb = aws("database/dynamodb", "DynamoDB · S3\nPITR · KMS")
    ext_api = aws("general/internet-alt1", "Approved\nthird-party APIs")

    with cluster("SHARED CONTROLS · protect + observe every layer", *SECURITY):
        sm = aws("security/secrets-manager", "⑧ Secrets Manager\nauto-rotation")
        kms = aws("security/key-management-service", "KMS\nper-data keys")
        ssm = aws("management/systems-manager", "⑨ Verified Access\n+ SSM sessions\nno SSH")
        gd = aws("security/guardduty", "⑩ GuardDuty\nruntime monitor")
        cw = aws("management/cloudwatch", "⑪ CloudWatch\nApp Signals · X-Ray")

    users >> FLOW() >> r53 >> FLOW() >> cf
    waf >> Edge(style="dashed", label="filters") >> cf
    shield >> Edge(style="dashed", label="shields") >> cf
    cf >> FLOW("③ VPC origin") >> alb >> FLOW() >> svc
    svc >> FLOW() >> [aur, val]
    svc >> FLOW("jobs") >> sqs >> FLOW() >> wrk
    [svc, wrk] >> FLOW() >> vpce >> FLOW() >> s3ddb
    svc >> FLOW("egress") >> nfw >> FLOW() >> ext_api
    [sm, kms, ssm, gd, cw] >> CONTROL() >> svc


# 4 · Detection and automated response ---------------------------------------
with diagram("4 · Threat detection and automated incident response", "04-detect-respond"):
    with cluster("① SIGNALS · every account", *NEUTRAL):
        trail = aws("management/cloudtrail", "CloudTrail")
        flow = aws("network/vpc-flow-logs", "VPC Flow Logs")
        dns = aws("network/route-53", "DNS query logs")
        eks = aws("compute/elastic-kubernetes-service", "EKS / ECS\nruntime agent")
        s3e = aws("storage/simple-storage-service-s3", "S3 data events")
    signals = [trail, flow, dns, eks, s3e]

    with cluster("② DETECTION · managed detectors", *SECURITY):
        gd = aws("security/guardduty", "GuardDuty\nthreats")
        insp = aws("security/inspector", "Inspector\nvulnerabilities")
        macie = aws("security/macie", "Macie\nsensitive data")
        cfg = aws("management/config", "AWS Config\nconfig drift")
        aa = aws("security/identity-and-access-management-iam-access-analyzer", "Access Analyzer\nexcess access")
    detectors = [gd, insp, macie, cfg, aa]

    lake = aws("security/security-lake", "⑧ Security Lake · OCSF")
    athena = aws("analytics/athena", "Athena · OpenSearch\nhunting · SIEM")
    hub = aws("security/security-hub", "③ Security Hub\nexposure findings")
    eb = aws("integration/eventbridge", "④ EventBridge\nroute by severity")

    with cluster("⑤ AUTOMATED PLAYBOOKS · seconds, not hours", *ACCOUNT):
        sfn = aws("integration/step-functions", "Step Functions")
        p1 = aws("compute/lambda", "Isolate workload\nquarantine SG")
        p2 = aws("security/identity-and-access-management-iam", "Revoke IAM\nsessions + keys")
        p3 = aws("storage/simple-storage-service-s3", "Block S3\npublic access")
        p4 = aws("security/waf", "Block attacker IP\nWAF IP set")

    with cluster("⑥ HUMANS IN THE LOOP", *VPC):
        q = aws("ml/q", "Amazon Q Developer\nin Slack / Teams")
        pd = ext("saas/alerting/pagerduty", "PagerDuty\non-call")

    detv = aws("security/detective", "⑦ Detective\ninvestigation graph")
    sir = aws("security/security-identity-and-compliance", "AWS Security\nIncident Response")
    pm = aws("management/organizations", "⑨ Post-incident\nnew SCP / rule\n/ pipeline gate")

    signals >> FLOW() >> gd
    trail >> Edge(style="dotted", color="#879196") >> lake >> FLOW() >> athena
    detectors >> FINDING() >> hub
    hub >> FLOW() >> eb
    eb >> FLOW("known pattern") >> sfn >> FLOW() >> [p1, p2, p3, p4]
    eb >> FLOW("needs a human") >> q
    q - pd
    hub >> FLOW() >> detv >> FLOW("escalate") >> sir
    detv >> FLOW() >> pm
    pm >> GOVERN("prevent it next time") >> cfg
