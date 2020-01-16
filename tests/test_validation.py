import pytest

from octokit import Base
from octokit import errors


class TestBase(object):

    def test_validate_required_parameters(self):
        attrs = {'owner': 'me', 'repo': 'my_repo'}
        assert Base().validate(attrs, self.parameter_only_definition)

    def test_raise_error_for_missing_required_parameter(self):
        attrs = {'owner': 'me'}
        with pytest.raises(errors.OctokitParameterError) as e:
            Base().validate(attrs, self.definition)
        assert 'repo is a required parameter' == str(e.value)

    def test_raise_error_for_missing_required_request_body_property(self):
        attrs = {'owner': 'me', 'repo': 'my_repo'}
        with pytest.raises(errors.OctokitParameterError) as e:
            Base().validate(attrs, self.definition)
        assert 'name is a required parameter' == str(e.value)
        attrs = {'owner': 'me', 'repo': 'my_repo', 'name': 'blah'}
        with pytest.raises(errors.OctokitParameterError) as e:
            Base().validate(attrs, self.definition)
        assert 'head_sha is a required parameter' == str(e.value)

    def test_validate_parameters_and_request_body_properties(self):
        attrs = {'owner': 'me', 'repo': 'my_repo', 'name': 'blah', 'head_sha': 'master'}
        assert Base().validate(attrs, self.definition)

    def test_validate_nested_request_body_properties(self):
        attrs = {'owner': 'me', 'repo': 'my_repo', 'name': 'blah', 'head_sha': 'master', 'output': {}}
        with pytest.raises(errors.OctokitParameterError) as e:
            Base().validate(attrs, self.definition)
        assert 'title is a required parameter' == str(e.value)
        attrs = {'owner': 'me', 'repo': 'my_repo', 'name': 'blah', 'head_sha': 'master', 'output': {'title': 'here'}}
        with pytest.raises(errors.OctokitParameterError) as e:
            Base().validate(attrs, self.definition)
        assert 'summary is a required parameter' == str(e.value)
        attrs = {'owner': 'me', 'repo': 'my_repo', 'name': 'blah', 'head_sha': 'master', 'output': {'title': 'here', 'summary': 'there'}}
        assert Base().validate(attrs, self.definition)

    @property
    def definition(self):
        return {"parameters": [
          {
            "name": "accept",
            "description": "This API is under preview and subject to change.",
            "in": "header",
            "schema": {
              "type": "string",
              "default": "application/vnd.github.antiope-preview+json"
            },
            "required": True
          },
          {
            "name": "owner",
            "description": "owner parameter",
            "in": "path",
            "required": True,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "repo",
            "description": "repo parameter",
            "in": "path",
            "required": True,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "The name of the check. For example, \"code-coverage\"."
                  },
                  "head_sha": {
                    "type": "string",
                    "description": "The SHA of the commit."
                  },
                  "details_url": {
                    "type": "string",
                    "description": "The URL of the integrator's site that has the full details of the check."
                  },
                  "external_id": {
                    "type": "string",
                    "description": "A reference for the run on the integrator's system."
                  },
                  "status": {
                    "type": "string",
                    "description": "The current status. Can be one of `queued`, `in_progress`, or `completed`.",
                    "enum": [
                      "queued",
                      "in_progress",
                      "completed"
                    ],
                    "default": "queued"
                  },
                  "started_at": {
                    "type": "string",
                    "description": "The time that the check run began. This is a timestamp in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format: `YYYY-MM-DDTHH:MM:SSZ`."
                  },
                  "conclusion": {
                    "type": "string",
                    "description": "**Required if you provide `completed_at` or a `status` of `completed`**. The final conclusion of the check. Can be one of `success`, `failure`, `neutral`, `cancelled`, `timed_out`, or `action_required`. When the conclusion is `action_required`, additional details should be provided on the site specified by `details_url`.  \n**Note:** Providing `conclusion` will automatically set the `status` parameter to `completed`.",
                    "enum": [
                      "success",
                      "failure",
                      "neutral",
                      "cancelled",
                      "timed_out",
                      "action_required"
                    ]
                  },
                  "completed_at": {
                    "type": "string",
                    "description": "The time the check completed. This is a timestamp in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format: `YYYY-MM-DDTHH:MM:SSZ`."
                  },
                  "output": {
                    "type": "object",
                    "description": "Check runs can accept a variety of data in the `output` object, including a `title` and `summary` and can optionally provide descriptive details about the run. See the [`output` object](https://developer.github.com/v3/checks/runs/#output-object) description.",
                    "properties": {
                      "title": {
                        "type": "string",
                        "description": "The title of the check run."
                      },
                      "summary": {
                        "type": "string",
                        "description": "The summary of the check run. This parameter supports Markdown."
                      },
                      "text": {
                        "type": "string",
                        "description": "The details of the check run. This parameter supports Markdown."
                      },
                      "annotations": {
                        "type": "array",
                        "description": "Adds information from your analysis to specific lines of code. Annotations are visible on GitHub in the **Checks** and **Files changed** tab of the pull request. The Checks API limits the number of annotations to a maximum of 50 per API request. To create more than 50 annotations, you have to make multiple requests to the [Update a check run](https://developer.github.com/v3/checks/runs/#update-a-check-run) endpoint. Each time you update the check run, annotations are appended to the list of annotations that already exist for the check run. For details about how you can view annotations on GitHub, see \"[About status checks](https://help.github.com/articles/about-status-checks#checks)\". See the [`annotations` object](https://developer.github.com/v3/checks/runs/#annotations-object) description for details about how to use this parameter.",
                        "items": {
                          "type": "object",
                          "properties": {
                            "path": {
                              "type": "string",
                              "description": "The path of the file to add an annotation to. For example, `assets/css/main.css`."
                            },
                            "start_line": {
                              "type": "integer",
                              "description": "The start line of the annotation."
                            },
                            "end_line": {
                              "type": "integer",
                              "description": "The end line of the annotation."
                            },
                            "start_column": {
                              "type": "integer",
                              "description": "The start column of the annotation. Annotations only support `start_column` and `end_column` on the same line. Omit this parameter if `start_line` and `end_line` have different values."
                            },
                            "end_column": {
                              "type": "integer",
                              "description": "The end column of the annotation. Annotations only support `start_column` and `end_column` on the same line. Omit this parameter if `start_line` and `end_line` have different values."
                            },
                            "annotation_level": {
                              "type": "string",
                              "description": "The level of the annotation. Can be one of `notice`, `warning`, or `failure`.",
                              "enum": [
                                "notice",
                                "warning",
                                "failure"
                              ]
                            },
                            "message": {
                              "type": "string",
                              "description": "A short description of the feedback for these lines of code. The maximum size is 64 KB."
                            },
                            "title": {
                              "type": "string",
                              "description": "The title that represents the annotation. The maximum size is 255 characters."
                            },
                            "raw_details": {
                              "type": "string",
                              "description": "Details about this annotation. The maximum size is 64 KB."
                            }
                          },
                          "required": [
                            "path",
                            "start_line",
                            "end_line",
                            "annotation_level",
                            "message"
                          ]
                        }
                      },
                      "images": {
                        "type": "array",
                        "description": "Adds images to the output displayed in the GitHub pull request UI. See the [`images` object](https://developer.github.com/v3/checks/runs/#images-object) description for details.",
                        "items": {
                          "type": "object",
                          "properties": {
                            "alt": {
                              "type": "string",
                              "description": "The alternative text for the image."
                            },
                            "image_url": {
                              "type": "string",
                              "description": "The full URL of the image."
                            },
                            "caption": {
                              "type": "string",
                              "description": "A short image description."
                            }
                          },
                          "required": [
                            "alt",
                            "image_url"
                          ]
                        }
                      }
                    },
                    "required": [
                      "title",
                      "summary"
                    ]
                  },
                  "actions": {
                    "type": "array",
                    "description": "Displays a button on GitHub that can be clicked to alert your app to do additional tasks. For example, a code linting app can display a button that automatically fixes detected errors. The button created in this object is displayed after the check run completes. When a user clicks the button, GitHub sends the [`check_run.requested_action` webhook](https://developer.github.com/v3/activity/events/types/#checkrunevent) to your app. Each action includes a `label`, `identifier` and `description`. A maximum of three actions are accepted. See the [`actions` object](https://developer.github.com/v3/checks/runs/#actions-object) description. To learn more about check runs and requested actions, see \"[Check runs and requested actions](https://developer.github.com/v3/checks/runs/#check-runs-and-requested-actions).\" To learn more about check runs and requested actions, see \"[Check runs and requested actions](https://developer.github.com/v3/checks/runs/#check-runs-and-requested-actions).\"",
                    "items": {
                      "type": "object",
                      "properties": {
                        "label": {
                          "type": "string",
                          "description": "The text to be displayed on a button in the web UI. The maximum size is 20 characters."
                        },
                        "description": {
                          "type": "string",
                          "description": "A short explanation of what this action would do. The maximum size is 40 characters."
                        },
                        "identifier": {
                          "type": "string",
                          "description": "A reference for the action on the integrator's system. The maximum size is 20 characters."
                        }
                      },
                      "required": [
                        "label",
                        "description",
                        "identifier"
                      ]
                    }
                  }
                },
                "required": [
                  "name",
                  "head_sha"
                ]
              },
            }
          }
        }
        }

    @property
    def parameter_only_definition(self):
        return {"parameters": [
          {
            "name": "accept",
            "description": "This API is under preview and subject to change.",
            "in": "header",
            "schema": {
              "type": "string",
              "default": "application/vnd.github.antiope-preview+json"
            },
            "required": True
          },
          {
            "name": "owner",
            "description": "owner parameter",
            "in": "path",
            "required": True,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "repo",
            "description": "repo parameter",
            "in": "path",
            "required": True,
            "schema": {
              "type": "string"
            }
          }
        ]}

