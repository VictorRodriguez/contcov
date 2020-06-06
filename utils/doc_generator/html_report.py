import json
import sys
import os
import operator


def print_html_report(report, title, img_name):
    """
    Print the html report
    """
    import jinja2

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "template.html"
    template = template_env.get_template(template_file)
    heads = ["Name", "Version", "Size"]
    heads_comp = ["Name", "Size", "Component"]
    output_text = template.render(pips=report["pips"],
                                  rpms=report["rpms"],
                                  apts=report["apts"],
                                  files_list=report["files"],
                                  heads=heads,
                                  heads_comp=heads_comp,
                                  img_name=img_name,
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

    filepath = 'components'
    components_new = []
    with open(filepath) as fp:
        components = fp.readlines()
    for comp in components:
        components_new.append(comp.strip())
    components = components_new

    pips = []
    rpms = []
    apts = []
    files_list = []

    for element in data:
        img_name = element["Image"]
        analyzetype = element["AnalyzeType"]
        if analyzetype == "Pip":
            for count in range(0, len(element["Analysis"])):
                pip_dict = {}
                pip_dict["Name"] = element["Analysis"][count]["Name"]
                pip_dict["Version"] = element["Analysis"][count]["Version"]
                pip_dict["Size"] = element["Analysis"][count]["Size"]
                pips.append(pip_dict)
        if analyzetype == "RPM":
            for count in range(0, len(element["Analysis"])):
                rpm_dict = {}
                rpm_dict["Name"] = element["Analysis"][count]["Name"]
                rpm_dict["Version"] = element["Analysis"][count]["Version"]
                rpm_dict["Size"] = element["Analysis"][count]["Size"]
                rpms.append(rpm_dict)
        if analyzetype == "Apt":
            for count in range(0, len(element["Analysis"])):
                apt_dict = {}
                apt_dict["Name"] = element["Analysis"][count]["Name"]
                apt_dict["Version"] = element["Analysis"][count]["Version"]
                apt_dict["Size"] = element["Analysis"][count]["Size"]
                apts.append(apt_dict)
        if analyzetype == "File":
            for count in range(0, len(element["Analysis"])):
                file_dict = {}
                name = element["Analysis"][count]["Name"]
                size = element["Analysis"][count]["Size"]
                for comp in components:
                    if comp in name:
                        file_dict["Name"] = name
                        file_dict["Size"] = size
                        file_dict["Component"] = comp
                        files_list.append(file_dict)

    pips.sort(key=operator.itemgetter('Size'))
    pips.reverse()

    rpms.sort(key=operator.itemgetter('Size'))
    rpms.reverse()

    apts.sort(key=operator.itemgetter('Size'))
    apts.reverse()

    report["pips"] = pips
    report["rpms"] = rpms
    report["apts"] = apts
    report["files"] = files_list

    print_html_report(report, title, img_name)


if __name__ == "__main__":
    main()