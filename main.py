import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder

st.write("JADE-LESBO")

# Read secrets from Streamlit
ssh_config = st.secrets["ssh"]
db_config = st.secrets["database"]

def get_engine_via_ssh():
    # Setup SSH tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_config["host"], ssh_config["port"]),
        ssh_username=ssh_config["user"],
        ssh_password=ssh_config.get("password"),
        remote_bind_address=(db_config["host"], db_config["port"])
    )

    tunnel.start()

    # Create a connection string
    connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@127.0.0.1:{tunnel.local_bind_port}/{db_config['database']}"

    # Create a database engine
    engine = create_engine(connection_string)
    
    return engine, tunnel

def run_query(query, engine):
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

# Streamlit app
st.title("LESBO IS MY WORLD")

st.write("This app connects to a MySQL database over an SSH tunnel and runs a simple query.")

query = "SELECT * FROM tsla LIMIT 5;"

if st.button("Run Query"):
    engine, tunnel = get_engine_via_ssh()
    try:
        result = run_query(query, engine)
        st.write(result)
    finally:
        tunnel.stop()

# If you want to display the result in a table format
if st.button("Display Query Result"):
    engine, tunnel = get_engine_via_ssh()
    try:
        result = run_query(query, engine)
        st.dataframe(result)
    finally:
        tunnel.stop()
