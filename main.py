from gql import gql, Client
from utils import t
import client

IGNORE_COLUMNS = ["DONE"]

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
    self.column_mapping = None
    self.client = client.get_client()
    # dont wanna search how to create column mappings
    self._set_old_new_project()
    self.build_column_mapping()
    
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
  
  def get_recent_pr_merges(self):
    pass

  def get_all_open_prs(self):
    query = gql(t(
      '''
      query { 
        repository(name:"$name",owner:"$owner") {
          pullRequests(orderBy:{field: CREATED_AT, direction: ASC}, first:100, states:OPEN) {
            nodes{
              title
              changedFiles
              additions
              deletions
              labels(first: 10) {
                edges {
                  node {
                    name
                  }
                }
              }
            }
          }
        }
      }
    ''', name=self.name, owner=self.owner))
    resp = self.client.execute(query)
    return resp["repository"]["pullRequests"]["nodes"]
    

  def get_project_columns(self, project_number):
    query = gql(t(
      '''
      query { 
      repository(name:"$name", owner:"$owner") {
        project(number: $project_number) {
          columns(first: 100) {
            nodes {
              id
              name
              }
            }
          }
        }
      }
    ''',name=self.name, owner=self.owner, project_number=project_number))
    resp = self.client.execute(query)
    return resp["repository"]["project"]["columns"]["nodes"]

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
      ''',
    name=self.name, owner=self.owner, project_number=project_number))

    resp = self.client.execute(query)
    return resp["repository"]["project"]["columns"]["nodes"]

  def _set_old_new_project(self):
    projects = self.get_last_two_project_details()
    self.old_project = projects[0]
    self.new_project = projects[1]

  def set_project_for_issue(self, issue_id, project_number):
    pass

  def set_column_for_issue(self, issue_id, column_id):
    pass

  def build_column_mapping(self):
    if self.column_mapping == None:
      old_columns = self.get_project_columns(self.old_project["number"])
      new_columns = self.get_project_columns(self.new_project["number"])
      print()
      print(self.old_project["number"]) 

c = OdoGHClient()
print(c.get_all_column_and_issue_ids(c.old_project["number"]))