from gql import gql, Client
from utils import t
import client


class Issue(object):
  def __init__(self, project_number, project_id, column_id, issue_id):
    super().__init__()
    self.project_number = project_number
    self.project_id = project_id
    self.column_id = column_id
    self.issue_id = issue_id


class OdoGHClient(object):
  def __init__(self):
    self.name = "odo"
    self.owner = "openshift"
    self.client = client.get_client()
    # dont wanna search how to create column mappings
    self._set_old_new_project()
    
  def get_last_two_project_details(self):
    query = gql(t(
      '''
      query { 
        repository(name:"$name", owner:"$owner") {
          projects(last:2) {
            nodes {
            number
            name
            id
            }
          }
        }
    }
    ''',name=self.name, owner=self.owner))
    resp = self.client.execute(query)
    return resp["repository"]["projects"]["nodes"]
  
  def get_project_columns(self, project_number):
    query = gql(t(
      '''
      query { 
      repository(name:"$name", owner:"$owner") {
        project(number: 100) {
          columns(first: 100) {
            nodes {
              id
              name
              }
            }
          }
        }
      }
    ''',name=self.name, owner=self.owner))
    resp = self.client.execute(query)
    return resp["repository"]["projects"]["columns"]["nodes"]

  def get_all_column_and_issue_ids(self, project_number):
    query = gql(t(
      '''
      query { 
        repository(name:"$name", owner:"$owner") {
          project(number: $project_number) {
            columns(first:100) {
              nodes {
                id
                name
                cards {
                  nodes{
                    content{
                      ... on Issue {
                      id
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      '''
    ),name=self.name, owner=self.owner)

    resp = self.client.execute(query)
    return resp["repository"]["projects"]["columns"]["nodes"]

  def _set_old_new_project(self):
    projects = self.get_last_two_project_details()
    self.old_project = projects[0]
    self.new_project = projects[1]

  def build_column_mapping(self, old_project, new_project):
    if self.column_mapping == None:
      pass

c = OdoGHClient()
c.get_last_two_project_details()