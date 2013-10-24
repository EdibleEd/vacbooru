# TAKES a set of tupples of the form
# {source_url, source_hash, [tags]}
# OPTIONALLY TAKES cull tags list, user name
# RETURNS a set of tupples of the form
# {source_url, source_hash, [tags]}

# A series of quality checking steps
# All do not alter the format of the data
# Steps projected are as follows:
# 1. Check if file is already uploaded
# 2. Cull file if it has certain tags
# 3. add user to tags
# 4. Add or remove existing tags
# 5. verify checksum is sane

class VAB_QC:
    pass
