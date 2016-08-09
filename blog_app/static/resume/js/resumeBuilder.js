/*
This is empty on purpose! Your code to build the resume will go here.
*/

/*var awesomeThoughts = "I am Hieu and I am AWESOME!"
var funThoughts = awesomeThoughts.replace("AWESOME", "FUN")
$("#main").append(funThoughts)*/

var skills = ["Python", "Flask", "Java"];

var bio = {
    "name" : "Le Trung Hieu",
    "role": "Junior Full Stack Developer",
    "contacts": {
        "mobile": "01672408495",
        "email": "letrunghieu37@gmail.com",
        "github": "https://github.com/bos-hieu",
        "location": "Ho Chi Minh City"
    },
    "welcomeMessage" : "Hello guys. My name's Trung Hieu and this is my resume.",
    "skills" : ["Python", "Flask", "HTML/CSS", "JavaScript", "Java"]
};

/*
var work = {
    "jobs": [
    {
        "employer": "VNG",
        "title": "Java InterShip",
        "location": "Ho Chi Minh",
        "dates": "2015-2016",
        "description": "Hello"
    },
    {
        "employer": "GCB",
        "title": "Python InterShip",
        "location": "Ho Chi Minh",
        "dates": "2014-2016",
        "description": "Goodbye"
    }
    ]
};
*/

var education = {
    "schools" : [
    {
        "name": "VNUHCM-University of Information Technology",
        "location": "Ho Chi Minh City",
        "dates": "9/2012 - 6/2017",
        "major": "Computer Sciene",
        "url": "http://www.uit.edu.vn/"
    }]
};

var projects = {
    "projects": [{
        "title": "My Blog",
        "dates": "7/2016 - 8/2016",
        "description": "This is blog project, with flask, python and postgresql. <br>Include several basic task such as: login, logout, show post, show user, profile,...",
        "images": [
            "static/resume/images/post_all.png",
            "static/resume/images/post_user.png"
        ],
        "url": "/post/all"
    }, {
        "title": "Resume",
        "dates": "8/2016",
        "description": "This is final project of the JavaScript Basic course",
        "images": ["static/resume/images/resume.png"],
        "url": "/resume"
    }]
}

// function display of 'bio' section
bio.display = function(){
    var formattedName = HTMLheaderName.replace("%data%", bio.name)
    var formattedRole = HTMLheaderRole.replace("%data%", bio.role)
    $("#header").prepend(formattedRole)
    $("#header").prepend(formattedName)

    //var formattedcontactGeneric = HTMLcontactGeneric.replace
    var formatedMobile = HTMLmobile.replace("%data%", bio.contacts.mobile);
    var formatedEmail =  HTMLemail.replace("%data%", bio.contacts.email);
    var formatedGithub =  HTMLgithub.replace("%data%", bio.contacts.github);
    var formatedLocation =  HTMLlocation.replace("%data%", bio.contacts.location);
    $("#topContacts").append(formatedMobile)
    $("#topContacts").append(formatedEmail)
    $("#topContacts").append(formatedGithub)
    $("#topContacts").append(formatedLocation)
    $("#footerContacts").append(formatedMobile)
    $("#footerContacts").append(formatedEmail)
    $("#footerContacts").append(formatedGithub)
    $("#footerContacts").append(formatedLocation)

    var srcImage = "static/resume/images/uit.png";
    var formatedBioPic = HTMLbioPic.replace("%data%", srcImage);
    var formatedWelcomeMsg = HTMLwelcomeMsg.replace("%data%", bio.welcomeMessage);

    $("#header").append(formatedBioPic)
    $("#header").append(formatedWelcomeMsg)

    if(bio.skills.length > 0){
        $("#header").append(HTMLskillsStart);

        for (i in bio.skills){
            var formatedSkill = HTMLskills.replace("%data%", bio.skills[i]);
            $("#skills").append(formatedSkill);
        }
    };
}
bio.display()

// function display of 'work' section
/*work.display = function(){
    if(work.jobs.length > 0){

        for(j in work.jobs){
            $("#workExperience").append(HTMLworkStart);

            var formatedEmployer = HTMLworkEmployer.replace("%data%", work.jobs[j].employer);
            var formatedTitle = HTMLworkTitle.replace("%data%", work.jobs[j].title);
            var formatedDates = HTMLworkDates.replace("%data%", work.jobs[j].dates);
            var formatedLocation = HTMLworkLocation.replace("%data%", work.jobs[j].location);
            var formatedDescription = HTMLworkDescription.replace("%data%", work.jobs[j].description);

            $(".work-entry:last").append(formatedEmployer + formatedTitle);
            $(".work-entry:last").append(formatedLocation);
            $(".work-entry:last").append(formatedDates);
            $(".work-entry:last").append(formatedDescription);
        }

    }
}

work.display()*/

//function display of "education" section
education.display = function(){
    if(education.schools.length > 0){
        for (s in education.schools){
            $("#education").append(HTMLschoolStart);

            var formatedSchoolName = HTMLschoolName.replace("%data%", education.schools[s].name)
            formatedSchoolName = formatedSchoolName.replace("%url%", education.schools[s].url)
            var formatedSchoolDates = HTMLschoolDates.replace("%data%", education.schools[s].dates)
            var formatedSchoolLocation = HTMLschoolLocation.replace("%data%", education.schools[s].location)
            var formatedSchoolMajor = HTMLschoolMajor.replace("%data%", education.schools[s].major)

            $(".education-entry:last").append(formatedSchoolName);
            $(".education-entry:last").append(formatedSchoolDates);
            $(".education-entry:last").append(formatedSchoolLocation);
            $(".education-entry:last").append(formatedSchoolMajor);
        }
    }
}
education.display()

//function display of 'project' section
projects.display = function(){
    if(projects.projects.length > 0){

        for (p in projects.projects){
            $("#projects").append(HTMLprojectStart)

            var formatedTitle = HTMLprojectTitle.replace("%data%", projects.projects[p].title);
            formatedTitle = formatedTitle.replace("%url%",projects.projects[p].url);
            var formatedDates = HTMLprojectDates.replace("%data%", projects.projects[p].dates);
            var formatedDescription = HTMLprojectDescription.replace("%data%", projects.projects[p].description);

            $(".project-entry:last").append(formatedTitle);
            $(".project-entry:last").append(formatedDates);
            $(".project-entry:last").append(formatedDescription);

            for (i in projects.projects[p].images){
                var formatedImage = HTMLprojectImage.replace("%data%", projects.projects[p].images[i]);
                $(".project-entry:last").append(formatedImage);}
            }
        }
    }
    projects.display()

    function inName(oldName){
        var finalName = oldName;
    // Your code goes here!
    var temp = finalName.split(" ")
    temp[0] = temp[0][0].toUpperCase() + temp[0].slice(1).toLowerCase()
    temp[1] = temp[1].toUpperCase()
    finalName = temp[0] + " " + temp[1]


    // Don't delete this line!
    return finalName;
}

//$("#main").append(internationalizeButton);

$("#mapDiv").append(googleMap);