import json
import re
from IPython import embed
from radish import before, after, world
from terraform_compliance.extensions.terraform import TerraformParser
from terraform_compliance.common.helper import Null

@before.each_feature
def load_terraform_data(feature):
    world.config.terraform = TerraformParser(world.config.user_data['plan_file'])


@before.each_step
def parse_in_step_variables(step):
    # ignore given steps (doesn't support match, would need to do something else for them, also there's no second stash)
    if step.context_class == 'given':
        return

    # if step doesn't have argument_match, it doesn't support in_step_variables
    if step.argument_match is None:
        return

    if step.context.bad_tags:
        return

    groupindex = dict(step.argument_match.match.match.re.groupindex)
    regs = step.argument_match.match.match.regs
    sentence = step.context_sensitive_sentence
    field_map = {field: sentence[regs[i][0]: regs[i][1]] for field, i in groupindex.items()}

    # ignore the regex statements
    if 'search_regex' in field_map:
        del field_map['search_regex']

    in_step_variables = {}
    match = step.context.match
    regex = r'(.*){(.*)}(.*)'

    for field, field_val in field_map.items():
        matches = match.regex_match(regex, str(field_val))
        if matches is None:
            continue
        
        query = matches.group(2).split('.')
        if not query:
            continue # do something here
        
        resource_type = query.pop(0)
        query_result = [resource for resource in step.context.cumulative_stash if match.equals(resource['type'], resource_type)]

        list_indexing_regex = r'\[([0-9]*)(:)?([0-9]*)\]' # accepts []
        for q in query:
            if not query_result:
                break
            
            list_indexing_match = match.regex_match(list_indexing_regex, q)
            if list_indexing_match and q != '[]':
                if not list_indexing_match.group(2):
                    # index from the first group
                    index = int(list_indexing_match.group(1))
                    query_result = [resource[index] for resource in query_result]
                else:
                    # slice
                    temp_query_result = query_result[:]
                    index1 = int(list_indexing_match.group(1)) if list_indexing_match.group(1) else 0
                    index2 = int(list_indexing_match.group(3)) if list_indexing_match.group(3) else len(temp_query_result)
                    temp_query_result = temp_query_result[index1:index2]

                    query_result = [item for resource in temp_query_result for item in resource]
                    
            else:
                query_result = [match.get(resource, q) for resource in query_result if match.contains(resource, q)]
        
        if matches.group(1) or matches.group(3):
            if not all(isinstance(resource, (str, bool, int, float)) for resource in query_result):
                raise TypeError("Improper in step variable usage. Can't mix affixes with non-str in step variabes.")
            
            query_result = [f'{matches.group(1)}{resource}{matches.group(3)}' for resource in query_result]

        in_step_variables[field] = query_result

    step.context.in_step_variables = in_step_variables

@after.each_step
def exclude_resources(step):
    if not hasattr(step.context, 'resources_to_exclude') or not step.context.resources_to_exclude:
        return 

    if step.context_class != 'given':
        return
    
    match = step.context.match
    resources_to_exclude = match.get(step.context.resources_to_exclude, step.context.name, {})
    bad_resource_indices = []
    # note O(n^2) runtime, but shouldn't be a problem at this scale
    for address in resources_to_exclude:
        for i, resource in enumerate(step.context.stash):
            if match.equals(resource['address'], address):
                bad_resource_indices.append(i)
    
    step.context.stash = [step.context.stash[i] for i in range(len(step.context.stash)) if i not in bad_resource_indices]


# debugging step should be always the last hooker
@after.each_step(order=1)
def wait_for_user_input(step):
    if world.config.user_data['debugging_mode_enabled'] == 'False':
        return

    cmd = 'cmd'
    while cmd != '':
        try:
            cmd = input(">> Press enter to continue")
        except EOFError:
            print()
            return
        
        if cmd == 'd':
            embed()
        elif cmd == 's':
            print(json.dumps(step.context.stash, indent=4))
        elif cmd != '':
            print(
                """
Commands
- s: prints stash
- d: opens Interactive Python
- h: prints commands
                """
            )


