from shared.application import ApplicationModule

auth_module = ApplicationModule("auth")
auth_module.import_from("auth.application.command")
auth_module.import_from("auth.application.query")
