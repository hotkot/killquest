from PIL import Image
im=Image.open('source-art/cage-v159/cage-raw.png').convert('RGBA');w,h=im.size
tiles=[]
for i in range(6):
 x,y=i%3,i//3
 tile=im.crop((round(x*w/3),round(y*h/2),round((x+1)*w/3),round((y+1)*h/2)))
 tiles.append(tile.crop(tile.getbbox()))
scale=416/max(t.height for t in tiles)
frames=[]
for tile in tiles:
 tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(512,512));frame.alpha_composite(tile,((512-tile.width)//2,480-tile.height));frames.append(frame)
# Keep the rigid cage identical during breathing, including its upper crossbar.
for i in range(1,4):
 interior=frames[i].crop((150,158,360,434));frames[i]=frames[0].copy();frames[i].paste(interior,(150,158))
for i,frame in enumerate(frames):frame.save(f'dist/assets/items/prison-cage-{i:02}.png')
# Real game-scale comparison, a shared ground line.
board=Image.new('RGBA',(760,340),(49,43,40,255))
cage=frames[0].resize((340,340),Image.Resampling.LANCZOS);board.alpha_composite(cage,(70,300-round(340*240/256)))
npc=Image.open('dist/assets/characters/rebel-guard-00.png').convert('RGBA');npc=npc.resize((round(448*.66404),round(448*.66404)),Image.Resampling.LANCZOS);board.alpha_composite(npc,(400,300-round(408*.66404)))
board.save('source-art/cage-v159/scale-preview.png')
