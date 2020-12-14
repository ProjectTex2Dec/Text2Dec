#Pattern based approach

def extract_dependency_relations(doc):
    dependencies = []
    #for each sentence there exits a root. if it is a VERB or AUX then we extract dependencies
    for action in filter(lambda w: (w.pos == VERB or w.pos == AUX) and w.dep_ in ("ROOT"), doc): #using verbs to identify subject and objs # for each sentence there will be one action verb, so sentences with no action verb are ignored
        print("main action:", action.text)
        print("dep of main action:",action.dep_)
        print("list of lefts:",[t.text for t in action.lefts])
        print("list of rights:",[t.text for t in action.rights])
        print("list of lefts:",[t.text for t in action.children])

        subjects = [] #for each verb multi subs possible
        objects = [] #for each verb multi objs possible

        sub_obj_swap = False

        if action.dep_ in ("ROOT"):
            #when sub + action + obj is mentioned active way eg; weight determines BMI value
            main_subjects = [w for w in action.lefts if w.dep_ == "nsubj"] #should be only one
            main_objects = [w for w in action.rights if w.dep_ == "dobj"] #should be only one
            pass_subjects =[w for w in action.lefts if w.dep_ == "nsubjpass"]
            print("Passvie subjects:", pass_subjects)
            causal_verbs = [w for w in action.rights if w.dep_ == "xcomp"]
            pre_verbs = [w for w in action.children if w.dep_ == "pcomp"]

            if main_subjects: #active sentence eg: A detmines B
                print("Statement Type ACTIVE")
                #extract subjects and objects
                main_sub = main_subjects[0]
                print("main_subject:",main_sub)
                subjects.append(main_sub)
                #does main_sub have children due to conjunction "and height"
                other_subjects = [child for child in main_sub.children if child.dep_ == "conj"]
                if other_subjects:
                    ##if children of children are conjs add them too
                    other_subject_childs = [child for child in other_subjects[0].children if child.dep_ == "conj"]
                    if other_subject_childs:
                            other_subjects.append(other_subject_childs[0])

                    print("other subjects:",other_subjects)
                    for child in other_subjects:
                        subjects.append(child)
                    print("All subjects",subjects)
                if main_objects:
                    main_obj = main_objects[0]
                    objects.append(main_obj)
                    #does main_obj have children due to conjunction "and BMI Level"
                    other_objects = [child for child in main_obj.children if child.dep_ == "conj"]
                    if other_objects:
                        ##if children of children are conjs add them too
                        other_object_childs = [child for child in other_objects[0].children if child.dep_ == "conj"]
                        if other_object_childs:
                            other_objects.append(other_object_childs[0])

                        print("other objects:",other_objects)
                        for child in other_objects:
                            objects.append(child)
                        print("All Objects",objects)
                else: #no objects detected then look for preps (right and left) or advcls (left and right)
                    preps =  [w for w in action.children if w.dep_ == "prep"] #should be only one
                    print("preps identified:",preps)

                    advcls =  [w for w in action.children if w.dep_ == "advcl"] #should be only one
                    print("advcls identified:", advcls)

                    if preps:
                        if preps[0].pos == SCONJ:
                            print("conditional statemetn detected")
                            sub_obj_swap = True
                        main_objects = [w for w in preps[0].children if w.dep_ == "pobj"] #should be only one
                    elif advcls: #tentelively an if then condition
                        subordinate_conjunctions = [w for w in advcls[0].children if w.dep_ == "mark" and w.pos == SCONJ] #should be only one
                        if subordinate_conjunctions:
                            print("conditional statemetn detected")
                            sub_obj_swap = True
                        main_objects = [w for w in advcls[0].children if w.dep_ == "nsubj"] #should be only one
                    if main_objects:
                        main_obj = main_objects[0]
                        objects.append(main_obj)

                if sub_obj_swap:
                    for obj in objects:
                        for sub in subjects:
                            dependencies.append((obj, action, sub))
                else:
                    for sub in subjects:
                        for obj in objects:
                            dependencies.append((sub, action, obj))


            elif pass_subjects: #no active subjects so looking for passive subjs
                print("Statement Type PASSIVE here")
                main_obj = pass_subjects[0] #identify the object here
                print("main object:",main_obj)
                objects.append(main_obj)

                #does main_obj have children due to conjunction "and height"
                other_objs = [child for child in main_obj.children if child.dep_ == "conj"]

                preps =  [w for w in action.children if w.dep_ == "prep"] #should be only one "from"
                print("Preps:", preps)
                if preps:
                    main_subjects = [w for w in preps[0].children if w.dep_ == "pobj"] #should be only one
                    print("Prep based main subjects:", main_subjects)
                    if not main_subjects:
                        pre_verbs = [w for w in preps[0].children if w.dep_ == "pcomp"]

                advcls =  [w for w in action.children if w.dep_ == "advcl"] #should be only one
                print("advcls identified:", advcls)
                other_verb_subjects = [] #for other advcls based subjs
                if advcls:
                    if not main_subjects: #no preps based subjects detected
                        main_subjects = [w for w in advcls[0].children if w.dep_ == "nsubj"]
                        print("advcls based new main subjs:",main_subjects)
                    else:
                        advcl_based_subjects = [w for w in advcls[0].children if w.dep_ == "nsubj"]
                        other_verb_subjects.append(advcl_based_subjects[0])
                    other_verbs = [child for child in advcls[0].children if child.dep_ == "conj"] #it is an AUX is
                    if other_verbs:
                        ##if children of children are conjs add them too
                        other_verb_childs = [child for child in other_verbs[0].children if child.dep_ == "conj"]
                        if other_verb_childs:
                            other_verbs.append(other_verb_childs[0])

                        print(other_verbs)

                        for verb in other_verbs:
                            for child in [w for w in verb.children if w.dep_ == "nsubj"]:
                                other_verb_subjects.append(child)

                if other_objs:
                    ##if children of children are conjs add them too
                    other_obj_childs = [child for child in other_objs[0].children if child.dep_ == "conj"]
                    if other_obj_childs:
                        other_objs.append(other_obj_childs[0])
                    print(other_objs)
                    for child in other_objs:
                            objects.append(child)
                    print("All objects",objects)

                if main_subjects:
                    main_sub = main_subjects[0]
                    print("main subject:", main_sub)
                    subjects.append(main_sub)
                    #does main_subj have children due to conjunction "and BMI Level"

                    other_subjects = [child for child in main_sub.children if child.dep_ == "conj"]

                    if other_subjects:
                        ##if children of children are conjs add them too
                        other_subject_childs = [child for child in other_subjects[0].children if child.dep_ == "conj"]
                        if other_subject_childs:
                            other_subjects.append(other_subject_childs[0])

                        print("other direct subjects:",other_subjects)
                        for child in other_subjects:
                            subjects.append(child)

                    if other_verb_subjects:
                        print("other verb based subjects:",other_verb_subjects)
                        for child in other_verb_subjects:
                            subjects.append(child)

                        print("All subjects",subjects)
                elif causal_verbs: #propagated objects
                    print("Using causal verbs")
                    main_subjects = [w for w in causal_verbs[0].children if w.dep_ == "dobj"]
                    if main_subjects:
                        temp = objects
                        objects = subjects
                        subjects = temp
                        objects.append(main_subjects[0])

                elif pre_verbs: #propagated objects
                    print("Using pcomp verbs")
                    main_subjects = [w for w in pre_verbs[0].children if w.dep_ == "dobj"]
                    if main_subjects:
                        #temp = objects
                        #objects = subjects
                        #subjects = temp
                        subjects.append(main_subjects[0])

                if objects:
                    for obj in objects:
                        for sub in subjects:
                            dependencies.append((sub, action, obj))
            elif main_objects:
                print("Statement Type Conditional")
                main_obj = main_objects[0]
                print("main_object:",main_obj)
                objects.append(main_obj)

                if action.children:
                    advcls =  [w for w in action.children if w.dep_ == "advcl"] #should be only one
                    print("advcls detected:",advcls)
                    csubjs =  [w for w in action.children if w.dep_ == "csubj"] #should be only csubj
                    print("csubjs detected:",csubjs)

                if advcls:
                    main_subjects = [w for w in advcls[0].children if w.dep_ == "nsubj"] #should be only one

                if csubjs:
                    main_subjects = [w for w in csubjs[0].children if w.dep_ == "nsubj"] #should be only one
                    if not main_subjects:
                        main_subjects = [w for w in csubjs[0].children if w.dep_ == "dobj"] #should be only one, it is an obj but it should go to subjects if no subj is aslready detected
                        print("clausal subject's object is detected")

                if main_subjects:
                        main_subj = main_subjects[0]
                        subjects.append(main_subj)

                if objects:
                    for obj in objects:
                        for sub in subjects:
                            dependencies.append((sub, action, obj))


        elif action.dep_ == "pobj" and action.head.dep_ == "prep":
            dependencies.append((action.head.head, money))
    return dependencies

#main()
