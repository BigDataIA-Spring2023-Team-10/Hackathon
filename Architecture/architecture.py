from diagrams import Diagram
from diagrams import Cluster, Edge, Node
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.gcp.analytics import Composer
from diagrams.onprem.client import Client
from diagrams.gcp.database import SQL
from diagrams.azure.web import AppServiceDomains
from diagrams.azure.web import APIConnections
from diagrams.gcp.storage import Storage

with Diagram("Architecture Diagram", show=False):
    ingress = Users("Users")
    with Cluster("Application"):
      with Cluster("Streamlit cloud"):
        streamlit = AppServiceDomains("Streamlit Cloud ")
      with Cluster("Google SQL"):
        db = SQL("SQL")
      with Cluster("OpenAI Services"):
        openai=APIConnections("OpenAI API")
      with Cluster("Cloud Storage"):
        storage = Storage("GCS")

  
    
    streamlit << Edge(label="Website") << ingress
    streamlit << Edge(label="Data Fetch") << db
    streamlit << Edge(label="Data Fetch") << storage 
    storage << Edge(label="Data Store") << streamlit
    openai << Edge(label="API Calls to ChatGPT") << streamlit

    streamlit << Edge(label="API Call Response") << openai    
    