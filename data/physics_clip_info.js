var speed = 100;
var width = 800; //width of the world  
var height = 600; //height of the world 
var scale = 60; //pixel to meter ratio; 1 meter = 60 pixels

var ballPositions = [];
//ballPositions = [A.x, A.y, A.linx, A.liny, B.x, B.y, B.linx, B.liny, E.x, E.y, E.linx, E.liny]
ballPositions[0] = [width + 75, 280,-1.2,-0.4,width + 155, 70,-1.3,0,width + 30,150,-1,-0];
ballPositions[1] = [width + 30, 450,-1,-0.6,width + 30, 100,-1,0.55,200,350,0,0];
ballPositions[2] = [width + 30, height-550,-1,0.45,width + 30, height-50,-1,-0.45,width/2-55,height/2,0,0];
ballPositions[3] = [width+270, 550,-1.3,-0.23,width + 250, 50,-1.1,0.2,width+30,410,-0.75,0];
ballPositions[4] = [200, 350,0,0,width + 30, 550,-1,-0.15,300,450,0,0];
ballPositions[5] = [width + 30, 550,-0.9,-0.4,width + 170, 220,-0.9,0.3,width + 120,500,-0.9,-0.4];
ballPositions[6] = [350, height/2,0,0,width + 30, height/2,-1,0,150,height/2,0,0];
ballPositions[7] = [width + 100, 550,-0.9,-0.3,width + 30, 150,-0.9,0.3,300,300,0,0];
ballPositions[8] = [width + 30, height/2,-0.9,0,width + 60, 550,-1.1,-0.3,100,height/2,0,0];
ballPositions[9] = [width + 30, 450,-0.9,-0.3,width + 100, 50,-1,0.5,300,300,0,0];
ballPositions[10] = [width + 100, 250,-1,0.6,width + 230, 540,-1.2,0,width + 30,450,-0.8,0];
ballPositions[11] = [width + 30, 300,-0.8,-0.5,width + 30, 550,-0.9,-0.3,width + 40,150,-0.9,0];
ballPositions[12] = [width + 30, 280,-0.9,0.06,width + 180, 550,-1.2,-0.4,100,height/2,0,0];
ballPositions[13] = [width + 200, 50,-1*1.04,0.5*1.04,width + 220, 500,-1.1,-0.45,width + 30,400,-0.8,-0.2];
ballPositions[14] = [width + 30, 430,-1,-0.15,width + 30, 170,-1,0.15,100,height/2,0,0];
ballPositions[15] = [width + 30, 430,-1,-0.18,width + 30, 170,-3/4,0.18*3/4,width/2-230,height/2,0,0];
ballPositions[16] = [width + 30, 50,-1,0.7,width + 120, 550,-1,-0.45,width + 30,300,-0.85,-0];
ballPositions[17] = [width + 40, 550,-0.8,-0.4,width + 30, 50,-0.7,0.5,width + 50,300,-0.8,-0];
ballPositions[18] = [width + 50, height-550,-1,0.45,width + 50, height-50,-1,-0.45,width + 30,height/2,-1,0];
ballPositions[19] = [width + 90, 500,-1,-0.4,width + 120, 50,-1*0.97,0.45*0.97,width + 30,350,-0.8,-0];
ballPositions[20] = [width + 60, 550,-1.1,-0.5,width + 165, 355,-1.2,-0.2,width + 30,350,-1,0];
ballPositions[21] = [80, 350,-0,-0,width + 100, 75,-1*0.9,0.4*0.9,width + 30,500,-0.8*1.1,-0.2*1.1];
ballPositions[22] = [width + 120, 50,-0.9,0.37,width + 360, 480,-1.3,-0.4,width+30,350,-0.79,0];
ballPositions[23] = [width+170, 50,-1,0.35,width + 250, 550,-1.1,-0.2,width+30,250,-0.75,0];
ballPositions[24] = [width + 230, 100,-1,0.3,width + 430, 600,-1.2*1.05,-0.35*1.05,width + 30,250,-0.8,0];
ballPositions[25] = [width + 80, 50,-1,0.7,80, 320,0,0,width + 30,300,-0.8,0];
ballPositions[26] = [width + 250, 150,-1.2,0.15,width + 130, 550,-1.2*0.8,-0.5*0.8,width + 30,250,-0.8,0];
ballPositions[27] = [width + 170, 500,-1,-0.23,100, 350,0,0,width + 30,200,-0.85,0.15];
ballPositions[28] = [width +250, 500,-1,-0.35,width + 430, 150,-1.2*1.05,0.25*1.05,width + 30,350,-0.8,0];
ballPositions[29] = [width + 120, 70,-0.9,0.08,400, 150,0,0,width + 30,250,-0.75,0];
ballPositions[30] = [width+350, height/2,-1,0,width + 600, height/2,-1.3,0,width+30,height/2,-0.75,0];
ballPositions[31] = [width+150, 50,-1,0.3,width + 200, 350,-1.1,-0.1,width+30,height/2,-0.75,0];

// for x/y positions: ballPositions/scale
// for linx/liny: ballPositions/scale*speed