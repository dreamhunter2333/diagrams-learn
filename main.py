from diagrams import Cluster, Diagram
from diagrams.k8s.network import Ingress
from diagrams.onprem.client import Users
from diagrams.azure.network import LoadBalancers
from diagrams.k8s.compute import Deployment, Cronjob, StatefulSet
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.azure.storage import StorageAccounts, BlobStorage, Azurefxtedgefiler
from diagrams.onprem.compute import Server


with Diagram(name="AWSL Architecture"):
    users = Users("Users")
    loadBalancer = LoadBalancers("LoadBalancer")
    ingress = Ingress("ingress")

    with Cluster("AKS"):
        mysql = Deployment("Mysql")
        sc = StorageClass("StorageClass")
        pvc = PVC("pvc")
        pv = PV("pv")
        mysql << pvc << pv << sc

        awsl_api = Deployment("awsl_api")
        awsl_front = Deployment("awsl_front")
        rabbitmq = StatefulSet("rabbitmq")
        rabbitmq << pvc

        discord_bot = Deployment("discord_bot")
        telebot = Deployment("telebot")

        ingress >> awsl_front >> awsl_api >> mysql

        awsl_wb_cron = Cronjob("awsl_wb_cron")
        awsl_wb_cron >> rabbitmq
        awsl_wb_cron >> mysql
        awsl_wb_cron << mysql

        azure_blob_cron = Cronjob("azure_blob_cron")
        azure_blob_cron >> mysql
        azure_blob_cron << mysql

        azure_blob_clean_cron = Cronjob("azure_blob_clean_cron")
        azure_blob_clean_cron >> mysql
        azure_blob_clean_cron << mysql

    awsl_storage = StorageAccounts("awsl StorageAccounts")
    awsl_blob = BlobStorage("awsl image blob")
    azure_file = Azurefxtedgefiler("azure file")
    azure_file >> sc
    awsl_storage << awsl_blob
    awsl_storage << azure_file

    azure_blob_cron >> awsl_blob
    azure_blob_clean_cron >> awsl_blob

    rabbitmq >> telebot >> Users("telegram channel")
    telegram_user = Users("telegram chat")
    telegram_user >> telebot >> telegram_user
    telebot >> awsl_api

    discord_user = Users("discord chat")
    discord_user >> discord_bot >> discord_user
    discord_bot >> awsl_api

    awsl_wb_cron >> Server("Wb Server")

    users >> loadBalancer >> ingress
    users >> awsl_blob
