from datetime import date
from flashy.sorting import sort
from flashy.spaced_rep import next_spaced_rep
from flask import Flask, request, redirect, url_for
import os.path
import csv

app = Flask(__name__)


def get_header():
    return """
       <head>
        <title>Flashy App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel='stylesheet' href='{stylesheet_url}'>
        <script src='{scripts_url}'></script>        
      </head>
    """.format(stylesheet_url=url_for('static', filename='css/style.css'), scripts_url=url_for('static', filename='scripts/flashy.js'))



@app.route("/subjects")
def hello_flashy():
    header = get_header()

    # are we creating a new subject
    new_subject = request.args.get('fsubject', '')

    # are we applying sort
    sort_by_choice = request.args.get('sort_by', '')

    # are we saving scores
    results_subject = request.args.get('rsubject', '')
    results_score = int(request.args.get('rscore', 0))

    new_subject_form = """
    <div class=\"new-subj-section\">
        <form action="/subjects">
         <label for="fsubject">New Subject:</label><br>
         <input type="text" id="fsubject" name="fsubject" size="40" ><br>
         <input type="submit" value="Save" class=\"new-elem-button\">
        </form> 
    </div>
    """

    sort_options_form = """
    <br>sort subjects:
    <form action="/subjects" >
     <input type="radio" id="default" name="sort_by" value="default" onchange="this.form.submit()" {default_checked} >
     <label for="default">default</label><br>
     <input type="radio" id="alphabetical" name="sort_by" value="alphabetical" onchange="this.form.submit()" {alpha_checked}>
     <label for="alphabetical">alpha</label>
     <!--input type="radio" id="card_no" name="sort_by" value="card_no" onchange="this.form.submit()" {card_no_checked}>
     <label for="card_no">by number of cards</label-->
    </form> 
    
    """.format(default_checked=(sort_by_choice=="default" and "checked" or ""),
               alpha_checked=(sort_by_choice=="alphabetical" and "checked" or "") ,
               card_no_checked=(sort_by_choice == "card_no" and "checked" or ""))

    subject_list = []

    with open("data/subjects.csv", 'r') as subjects_file_for_read:
        subject_reader = csv.reader(subjects_file_for_read, delimiter=',', quotechar='"')
        for row in subject_reader:
            subject_list.append({"subject": row[0], "stage": int(row[1]),
                                 "last": date.fromisoformat(row[2]) if row[2] else None })

    # save new subject
    if (new_subject != ''):
        if new_subject not in [x["subject"] for x in subject_list]:
            with open('data/subjects.csv',
                      ('a' if os.path.isfile('data/subjects.csv') else 'w')) as subjects_file_for_write:
                subject_writer = csv.writer(subjects_file_for_write, delimiter=',', quotechar='"')
                subject_writer.writerow([new_subject, 0, None])
                # we also add it to the in-memory list
                subject_list.append({"subject": new_subject, "stage": 0, "last": None})

    # saving results
    if (results_subject != ''):
        with open('data/subjects.csv','w') as subjects_file_for_write:
            subject_writer = csv.writer(subjects_file_for_write, delimiter=',', quotechar='"')
            for item in subject_list:
                if item["subject"].strip().replace(" ", "_")==results_subject:
                    item["last"] = date.today()
                    if(results_score>=50):
                        item["stage"]= item["stage"] + 1
                    else:
                        if item["stage"]>0:
                            item["stage"] = item["stage"] - 1
                subject_writer.writerow([item["subject"], item["stage"], item["last"]])

    # sorting
    if(sort_by_choice == "alphabetical" ):
        sort(subject_list)


    #format as html
    page_parts = [ header + "<h1>BB's Flashy app</h1>  <br> <table>",
                    "<tr><th>Subject</th><th>Next practice</th><th>Stage</th><th>last practice</th></tr>",
                     "".join(["<tr><td><a href=\"subject/" + x["subject"].strip().replace(" ", "_") + "\">" +
                                  x["subject"].strip()+ "</a> </td><td>" +
                                  str(next_spaced_rep(x["stage"],(x["last"] if x["last"] else date.today())))+
                                  "</td><td> " + str(x["stage"]) +
                                  "</td><td>" + (str(x["last"]) if x["last"] else "") + "</td></tr>"
                                  for x in subject_list]), "</table>",
                     sort_options_form, new_subject_form ]

    return "".join(page_parts)

@app.route("/subject/<name>")
def hello(name):
    # are we adding new q and a?
    new_q = request.args.get('fquestion', '')
    new_a = request.args.get('fanswer', '')

    question_list = []
    if (new_q!=''):
        with open("data/" + name + ".csv", ('a' if os.path.isfile("data/" + name + ".csv") else 'w')) as questions_file_for_write:
            q_n_a_writer = csv.writer(questions_file_for_write, delimiter=',', quotechar='"')
            q_n_a_writer.writerow([new_q,new_a])

    if os.path.isfile("data/" + name + ".csv"):
        with open("data/" + name + ".csv",'r') as questions_file_for_read:
            q_n_a_reader = csv.reader(questions_file_for_read, delimiter=',', quotechar='"')
            for row in q_n_a_reader:
                question_list.append({ "q": row[0], "a": row[1]} )


    new_card_form = """
    <div class=\"new-card-section\">
        <a href=\"../subjects\"> ⬅️ Back to subject list... </a>
        <br><br>...or add a new card <br><br>
        <form action="/subject/{subject}">
         <label for="fquestion">Question:</label><br>
         <input type="text" id="fquestion" name="fquestion" size="42"><br>
         <label for="fanswer">Answer:</label><br>
         <input type="text" id="fanswer" name="fanswer"size="42"><br>
         <input type="submit" value="Save" class=\"new-elem-button\">
        </form> 
    </div>
        """.format(subject=name)

    title = "<div class=\"cards-title\">Studying " + name.replace("_"," ") + "...  </div><br>"
    if len(question_list)> 0:
        title += "<div id=\"start-block\"><br> ready for a " + str(len(question_list)) + " card test? " \
                 "<button class=\"go-button\" onclick=\"go(" + str(len(question_list)) + ");\">GO!</button></div>"
    else:
        title += "<div id=\"start-block\"><br> you need to add some cards to this subjects in order to practice. " \
                 "See below.</div>"

    cards = []

    cards.append("<br><br><br><div id=\"card-container\">")
    for i in range(len(question_list)):
        cards.append("<div class=\"card\" id=\"card-" + str(i) + "\" style=\"visibility: hidden;\">")
        cards.append("  <div class=\"cardtext\" id=\"cardtext-" + str(i) + "\">" + question_list[i]["q"] + "</div>")
        cards.append("  <div class=\"buttonset\" id=\"rightwrong-" + str(i) + "\" style=\"visibility: hidden;\">")
        cards.append("    <button  class=\"card-button right-button\" id=\"right-" + str(i) + "\" onclick=\"right(" + str(i) + ");\">right</button>")
        cards.append("    <button  class=\"card-button wrong-button\" id=\"wrong-" + str(i) + "\" onclick=\"wrong(" + str(i) + ");\">wrong</button>")
        cards.append("  </div>")
        cards.append("  <div class=\"buttonset\"> <button  class=\"card-button\" id=\"reveal-button\" onclick=\"revealAnswer(" + str(i) + ",'" + question_list[i]["a"] +"');\">reveal answer</button></div>")
        cards.append("</div>")
        cards.append("<div id=\"results-block\" style=\"visibility: hidden;\">")
        cards.append("  <div id=\"results-text-message\"></div>")
        cards.append("  <a id=\"results-save-link\" href=\"../subjects?rsubject=" + name + "&rscore=\">save to my learning history</a>")
        cards.append("</div>")
    cards.append("</div>")



    return get_header() + title  + "".join(cards) + new_card_form
