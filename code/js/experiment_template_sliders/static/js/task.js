/* task.js
 * 
 * This file holds the main experiment code.
 * 
 * Requires:
 *   config.js
 *   psiturk.js
 *   utils.js
 */

// Create and initialize the experiment configuration object
var $c = new Config(condition, counterbalance);

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc);

// Preload the HTML template pages that we need for the experiment
psiTurk.preloadPages($c.pages);

// Objects to keep track of the current phase and state
var CURRENTVIEW;
var STATE;

/*************************
 * INSTRUCTIONS         
 *************************/

var Instructions = function() {

    // The list of pages for this set of instructions
    this.pages = $c.instructions.pages;

    // Display a page of instructions, based on the current
    // STATE.index
    this.show = function() {
        debug("show slide " + this.pages[STATE.index]);

        // Load the next page of instructions
        $(".slide").hide();
        var slide = $("#" + this.pages[STATE.index]);
        slide.fadeIn($c.fade);

        // Bind a handler to the "next" button. We have to wrap it in
        // an anonymous function to preserve the scope.
        var that = this;
        slide.find('.next').click(function () {
            that.record_response();
        });

    };

    // Handler for when the "next" button is pressed
    this.record_response = function() {
        // Go to the next page of instructions, or complete these
        // instructions if there are no more pages
        if ((STATE.index + 1) >= this.pages.length) {
            this.finish(); 
        } else {
            STATE.set_index(STATE.index + 1);
            this.show();
        }
    };

    // Clean up the instructions phase and move on to the test phase
    this.finish = function() {
        // debug("Done with instructions") ;

        // Record that the user has finished the instructions and
        // moved on to the experiment. This changes their status
        // code in the database.
        psiTurk.finishInstructions();

        // Reset the state object for the test phase
        STATE.set_instructions(0);
        STATE.set_index();
        CURRENTVIEW = new TestPhase();
    };

    // Display the first page of instructions
    this.show();
};



/*****************
 *  TRIALS       *
 *****************/

var TestPhase = function() {
    /* Instance variables */
    
    // Information about the current trial
    this.trialinfo;    
    // The response they gave
    this.response;
    // The number they've gotten correct, so far
    this.num_correct = 0;

    // Initialize a new trial. This is called either at the beginning
    // of a new trial, or if the page is reloaded between trials.
    this.init_trial = function () {
        debug("Initializing trial " + STATE.index);

        // If there are no more trials left, then we are at the end of
        // this phase
        if (STATE.index >= $c.trials.length) {
            this.finish();
            return false;
        }
        
        // Load the new trialinfo
        this.trialinfo = $c.trials[STATE.index];

        // Update progress bar
        update_progress(STATE.index, $c.trials.length);

        return true;
    }; 

    this.display_stim = function (that) {
        if (that.init_trial()) {
            debug("Show STIMULUS");
            
            // Show video
            video_name = that.trialinfo.name, 
            $("#video_mp4").attr("src",'/static/videos/mp4/' + video_name + '.mp4');
            $("#video_webm").attr("src",'/static/videos/webm/' + video_name + '.webmsd.webm');
            $("#video_ogg").attr("src",'/static/videos/ogg/' + video_name + '.oggtheora.ogv');
            $(".stim_video").load()
            
            $("#play.next").click(function () {
                $(".stim_video").load()
                $('.stim_video').trigger('play');
            });


            // Replace the name with the piece from the template
            // select a random name from the choices
            // var view = {
            //     'name': that.trialinfo.name
            // } ;
            
            // $('.stim_text').html(Mustache.render($c.text, view)) ;

            debug($c.questions) ;

            // Create the HTML for the question and slider.
            var html = "" ; 
            for (var i=0; i<$c.questions.length; i++) {
                // var q = Mustache.render($c.questions[i].q, view);
                var q = $c.questions[i].q;
                // html += '<p class=".question">' + (i+1) + '. ' + q +'</p><div class="s-'+i+'"></div><div class="l-'+i+'"></div><br />' ;
                html += '<p class=".question">' + q +'</p><div class="s-'+i+'"></div><div class="l-'+i+'"></div><br />' ;
            }
            $('#choices').html(html) ;

            // Bulid the sliders for each question
            for (var i=0; i<$c.questions.length; i++) {
                // Create the sliders
                $('.s-'+i).slider().on("slidestart", function( event, ui ) {
                    // Show the handle
                    $(this).find('.ui-slider-handle').show() ;

                    // Sum is the number of sliders that have been clicked
                    var sum = 0 ;
                    for (var j=0; j<$c.questions.length; j++) {
                        if ($('.s-'+j).find('.ui-slider-handle').is(":visible")) {
                            sum++ ;
                        }
                    }
                    // If the number of sliders clicked is equal to the number of sliders
                    // the user can continue. 
                    if (sum == $c.questions.length) {
                        $('#trial_next').prop('disabled', false) ;
                    }
                });
                                       
                // Put labels on the sliders
                $('.l-'+i).append("<label style='width: 33%'>"+ $c.questions[i].l[0] +"</label>") ; 
                $('.l-'+i).append("<label style='width: 33%'>"+ $c.questions[i].l[1] +"</label>") ; 
                $('.l-'+i).append("<label style='width: 33%'>"+ $c.questions[i].l[2] +"</label>");
            }

            // Hide all the slider handles 
            $('.ui-slider-handle').hide() ;

            // Disable button which will be enabled once the sliders are clicked
            $('#trial_next').prop('disabled', true);

            debug(that.trialinfo);
        }        
    };


    // Record a response (this could be either just clicking "start",
    // or actually a choice to the prompt(s))
    this.record_response = function() {        
        // TODO MAKE THIS CORRECT!
        var response = [] ;
        for (var i=0; i<$c.questions.length; i++) {
            response.push($('.s-'+i).slider('value')) ;
        }

        var question = $c.questions.map(function (question) {return question.type});
        
        psiTurk.recordTrialData([this.trialinfo.name, question[0], response[0],question[1], response[1], question[2], response[2],])

        STATE.set_index(STATE.index + 1);
        
        // Update the page with the current phase/trial
        this.display_stim(this);
    };

     this.finish = function() {
        debug("Finish test phase");

        // Change the page
        CURRENTVIEW = new Demographics()
    };

    // Load the trial html page
    $(".slide").hide();

    // Show the slide
    var that = this; 
    $("#trial").fadeIn($c.fade);
    $('#trial_next.next').click(function () {
        that.record_response();
    });


    // Initialize the current trial
    if (this.init_trial()) {
        // Start the test
        this.display_stim(this) ;
    };
};

/*****************
 *  DEMOGRAPHICS*
 *****************/

 var Demographics = function(){

// Complete the set of trials in the test phase
    
    this.finish = function() {
        debug("Finish test phase");

        // If we're at the end of the experiment, submit the data to
        // mechanical turk, otherwise go on to the next experiment
        // phase and show the relevant instructions

        // Show a page saying that the HIT is resubmitting, and
        // show the error page again if it times out or error
        var resubmit = function() {
            $(".slide").hide();
            $("#resubmit_slide").fadeIn($c.fade);

            var reprompt = setTimeout(prompt_resubmit, 10000);
            psiTurk.saveData({
                success: function() {
                    clearInterval(reprompt); 
                    finish();
                }, 
                error: prompt_resubmit
            });
        };

        // Prompt them to resubmit the HIT, because it failed the first time
        var prompt_resubmit = function() {
            $("#resubmit_slide").click(resubmit);
            $(".slide").hide();
            $("#submit_error_slide").fadeIn($c.fade);
        };

        // Render a page saying it's submitting
        psiTurk.showPage("submit.html") ;
        psiTurk.saveData({
            success: psiTurk.completeHIT, 
            error: prompt_resubmit
        });
    };

    psiTurk.showPage("demographics.html");
    var that = this;

    $('.next').click(function () {
            // save the gender age comments here using recorddata
            var gender = $('input[name = sex]:checked').val(); 
            var age = $('input[name = age]').val();
            var feedback = $('textarea[name = feedback]').val();
            psiTurk.recordUnstructuredData('gender',gender);
            psiTurk.recordUnstructuredData('age',age);
            psiTurk.recordUnstructuredData('feedback',feedback);            
            that.finish();
    });
 };


// --------------------------------------------------------------------
// --------------------------------------------------------------------

/*******************
 * Run Task
 ******************/

$(document).ready(function() { 
    // Load the HTML for the trials
    psiTurk.showPage("trial.html");

    // Record various unstructured data
    psiTurk.recordUnstructuredData("condition", condition);
    psiTurk.recordUnstructuredData("counterbalance", counterbalance);
   // psiTurk.recordUnstructuredData("choices", $("#choices").html());

    // Start the experiment
    STATE = new State();
    // Begin the experiment phase
    if (STATE.instructions) {
        CURRENTVIEW = new Instructions();
    } else {
        CURRENTVIEW = new TestPhase();
    }
});
