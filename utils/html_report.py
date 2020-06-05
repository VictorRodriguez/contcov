import json
import sys
import os

def print_html_report(report, title):
    """
    Print the html report
    """
    import jinja2

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "template.txt"
    template = template_env.get_template(template_file)
    heads = ["Name","Version","Size"]
    output_text = template.render(pkgs=report["pkgs"],\
        heads=heads,\
        title=title)
    report_title = 'report_%s.html' % (title)
    html_file = open(report_title, 'w')
    html_file.write(output_text)
    html_file.close()

def error_msg():
    print("Error")

def main():
    """
    main function
    """
    report = {}
    data = {}
    title = "test"
    if len(sys.argv) < 3:
        print("\nERROR : Missing arguments, the expected arguments are:")
        print("\n   %s <result.json> <title>\n" % (sys.argv[0]))
        print("\n")
        sys.exit(0)

    if os.path.isfile(sys.argv[1]):
        results_json = sys.argv[1]
    else:
        error_msg()
        sys.exit(0)

    title = sys.argv[2]

    try:
        with open(results_json) as json_file:
            data = json.load(json_file)
    except ValueError as error:
        print(error)

    pkgs = []
    for element in data:
        for count in range(0,len(element["Analysis"])):
            pkg_dict = {}
            pkg_dict["Name"]=element["Analysis"][count]["Name"]
            pkg_dict["Version"]=element["Analysis"][count]["Version"]
            pkg_dict["Size"]=element["Analysis"][count]["Size"]
            pkgs.append(pkg_dict)
    report["pkgs"] = pkgs
    print_html_report(report,title)

if __name__ == "__main__":
    main()
