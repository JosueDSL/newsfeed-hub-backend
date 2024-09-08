# Description: Helper methods for handling exceptions and creating error responses.

# Import the necessary libraries
from flask import make_response, jsonify, current_app as app



class ErrorHandler:
    """
    A class to handle exceptions and create error responses.
    """

    @staticmethod
    def make_error_response(error_message, status_code=400):
        """
        Create an error JSON response with a given error message and status code.

        Args:
            error_message (str): The error message to include in the response.
            status_code (int, optional): The HTTP status code for the response. Defaults to 400.

        Returns:
            Response: A Flask response object with the error message and status code.
        """
        response = make_response(jsonify({'error': {'message': error_message}}), status_code)
        return response


    @staticmethod
    def handle_general_exception(e):
        """
        Handle exceptions raised during a request.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A Flask response object with the error message and a 500 status code.
        """
        app.logger.error(str(e), exc_info=True)
        response = {
            "error": str(e),
            "message": "An error occurred."
        }
        return jsonify(response), 500


    @staticmethod
    def handle_exceptions(func):
        """
        Handle the errors that may arise during the execution of a function.

        Args:
            func (function): The function to execute.

        Returns:
            Any: The result of the function if no errors are raised.
            Response: A Flask response object with the error message and status code if an error is raised.
        """
        try:
            return func()
        except ValueError as e:
            app.logger.error('ValueError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except TypeError as e:
            app.logger.error('TypeError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except AttributeError as e:
            app.logger.error('AttributeError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except KeyError as e:
            app.logger.error('KeyError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except IOError as e:
            app.logger.error('IOError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except RuntimeError as e:
            app.logger.error('RuntimeError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except ZeroDivisionError as e:
            app.logger.error('ZeroDivisionError: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 400)
        except Exception as e:
            app.logger.error('An error occurred: %s', e, exc_info=True)
            return ErrorHandler.make_error_response(str(e), 500)