Django Custom Permissions & Groups Setup
This project implements custom permissions and group-based authorization to restrict access to various parts of the application.
Custom Permissions
Defined in models.py under the Book model:
can_view — User can view book records
can_create — User can create book records
can_edit — User can edit book records
can_delete — User can delete book records
Groups Setup
Configured manually via Django Admin:
Group	Permissions
Viewers	can_view
Editors	can_view, can_create, can_edit
Admins	can_view, can_create, can_edit, can_delete
Permissions in Views
Used the @permission_required decorator: