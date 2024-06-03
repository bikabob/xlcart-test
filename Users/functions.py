def gene_errors(form):
    messege = ""
    for field in form:
        if field.errors:
            messege += field.errors
    for err in form.non_field_errors():
        messege += str(err)
        
    return messege