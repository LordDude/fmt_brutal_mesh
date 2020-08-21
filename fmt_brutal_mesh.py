#Noesis Python model import+export test module, imports/exports some data from/to a made-up format

from inc_noesis import *

import noesis
import operator
import array
import itertools

#rapi methods should only be used during handler callbacks
import rapi

#registerNoesisTypes is called by Noesis to allow the script to register formats.
#Do not implement this function in script files unless you want them to be dedicated format modules!
def registerNoesisTypes():
   handle = noesis.register("Brutal Legend", ".header")
   noesis.setHandlerTypeCheck(handle, noepyCheckType)
   noesis.setHandlerLoadModel(handle, noepyLoadModel) #see also noepyLoadModelRPG
       #noesis.setHandlerWriteModel(handle, noepyWriteModel)
       #noesis.setHandlerWriteAnim(handle, noepyWriteAnim)
   noesis.logPopup()
       #print("The log can be useful for catching debug prints from preview loads.\nBut don't leave it on when you release your script, or it will probably annoy people.")
   return 1

NOEPY_HEADER = "hsem"

#check if it's this type based on the data
def noepyCheckType(data):
   bs = NoeBitStream(data)
   if len(data) < 16:
      return 1
   if bs.readString() != NOEPY_HEADER:
      return 0
   return 1


def RigStuff(VertBuffType, topname):
   #print("Loading Rig")
   RigExists = rapi.checkFileExists(topname+str(".Rig.header"))
   if RigExists:
      rigFile = rapi.loadIntoByteArray(topname+str(".Rig.header"))
   else:
      rigFile = rapi.loadPairedFile("Brutal Legend", ".Rig.header")
   rig = NoeBitStream(rigFile)
   Blank2 = rig.readUInt()
   Float1 = rig.readHalfFloat()
   Float2 = rig.readHalfFloat()
   Float3 = rig.readHalfFloat()
   Float4 = rig.readHalfFloat()
   BoneNameSize = rig.readUInt()
   BoneCount = rig.read("L")
   rig.seek(-4, NOESEEK_REL)
   BoneCount2 = rig.readUInt()
   parentIndicesSize = rig.readUInt()
   FlexCount = rig.readUInt()
   UNK5 = rig.readUInt()
   UNK6 = rig.readUInt()
   UNK7 = rig.readUInt()
   UNK8 = rig.readUInt()
   UNK9 = rig.readUInt()
   UNK10 = rig.readUInt()
   UNK11 = rig.readUInt()
   Float6 = rig.readFloat()
   UNK12 = rig.readUInt()
   UNK13 = rig.readUInt()
   UNK14 = rig.readUInt()
   rig.seek(76, NOESEEK_ABS)
   Offset1 = rig.readUInt()
   Offset2 = rig.readUInt()
   Offset3 = rig.readUInt()
   Offset4 = rig.readUInt()
   Offset5 = rig.readUInt()
   Offset6 = rig.readUInt()
   Offset7 = rig.readUInt()
   Blank2 = rig.readUInt()
   RigSig = rig.readUInt()
   BoneNames = []
   BoneParent = []
   BoneID = []
   boneList = []
   BoneXROTList = []
   BoneYROTList = []
   BoneZROTList = []
   BoneXSCAList = []
   BoneYSCAList = []
   BoneZSCAList = []
   BoneWSCAList = []
   BoneXPOSList = []
   BoneYPOSList = []
   BoneZPOSList = []
   BoneWPOSList = []
   FlexNames = []
   RigSourceExists = rapi.checkFileExists(topname+str(".Rig"))
   if RigSourceExists:
      rigSource = rapi.loadIntoByteArray(topname+str(".Rig"))
   else:
      rigSource = rapi.loadPairedFile("Brutal Legend", ".Rig")
   rigsource = NoeBitStream(rigSource)
   for i in range(0, BoneCount2):
      BoneNames.append (rigsource.readString())
   #rigsource.seek(0, NOESEEK_ABS)
   for i in range(0, FlexCount):
      FlexNames.append (rigsource.readString())
   print(FlexNames)
   rigsource.seek(Offset2, NOESEEK_ABS)
   for i in range(0, BoneCount[0]):
      BoneParent.append (rigsource.readShort())
   rigsource.seek(Offset6, NOESEEK_ABS)
   boneReList = []
   quat = NoeQuat([0, 0, 0, 0])
   turn = NoeQuat([0, 0, 0, 1])
   SCAINV = NoeVec3([0, 0, 0])
   SCA = NoeVec3([0, 0, 0])
   POS = NoeVec3([0, 0, 0])
   #print("BoneParent", BoneParent)
   for i in range(0, (BoneCount[0])):
      boneMat = NoeMat44.fromBytes(rigsource.readBytes(64))
      boneMat = boneMat.toMat43()
      boneMat = boneMat.inverse()
      boneReList.append (NoeBone(i, BoneNames[i], boneMat, None, BoneParent[i]))
   return boneReList


def VertStuff(bs, VertCount, VertBuffType):
   POS = bytearray()
   NORM = bytearray()
   UV1 = bytearray()
   UV2 = bytearray()
   TAN = bytearray()
   COL1 = bytearray()
   COL2 = bytearray()
   BI = bytearray()
   BW = bytearray()
   print(VertCount, VertBuffType)
   for V in range(0, VertCount):
      if VertBuffType == int(1024):
         BI += bs.readBytes(4)
         BW += bs.readBytes(4)
         POS += bs.readBytes(8)
         UV1 += bs.readBytes(4)
         UV2 += bs.readBytes(4)
         NORM += bs.readBytes(8)
         TAN += bs.readBytes(8)
         COL1 += bs.readBytes(4)
         COL2 += bs.readBytes(4)
      elif VertBuffType == int(768):
         POS += bs.readBytes(12)
         NORM += bs.readBytes(12)
         TAN += bs.readBytes(12)
         UV1 += bs.readBytes(8)
         UV2 += bs.readBytes(8)
         COL1 += bs.readBytes(4)
         COL2 += bs.readBytes(4)
         BI += bs.readBytes(4)
         BW += bs.readBytes(16)
      elif VertBuffType == int(512):
         POS += bs.readBytes(8)
         NORM += bs.readBytes(8)
         TAN += bs.readBytes(8)
         UV1 += bs.readBytes(4)
         UV2 += bs.readBytes(4)
         COL1 += bs.readBytes(4)
         COL2 += bs.readBytes(4)
      elif VertBuffType == int(256):
         POS += bs.readBytes(12)
         NORM += bs.readBytes(12)
         TAN += bs.readBytes(12)
         UV1 += bs.readBytes(8)
         UV2 += bs.readBytes(8)
         COL1 += bs.readBytes(4)
         COL2 += bs.readBytes(4)
      else:
         raise ValueError("Unknown VertBuffType", VertBuffType)
   return POS, NORM, TAN, UV1, UV2, COL1, COL2, BI, BW

#load the model

#MDL Header Stuff
def noepyLoadModel(data, mdlList):
   LOADANIM = 0
   ExportSkin = 1
   VertexBool = 0 #Vertex Bool = 1 is Vertex Tint Channel Vertex Bool = 0 is Material Layers
   #Remember Vertex Colors are BGRA
   ctx = rapi.rpgCreateContext()
   bs = NoeBitStream(data)
   rapi.rpgSetOption(noesis.RPGOPT_MORPH_RELATIVEPOSITIONS, 1)
   rapi.rpgSetOption(noesis.RPGOPT_MORPH_RELATIVENORMALS, 1)
   #IDSig = bs.readUInt()
   #Blank1 = bs.readUInt()
   #BSphereX = bs.readFloat()
   #BSphereY = bs.readFloat()
   #BSphereZ = bs.readFloat()
   #BSphereThing = bs.readFloat()
   #UNK1 = bs.readFloat()
   #BBoxX1 = bs.readFloat()
   #BBoxY1 = bs.readFloat()
   #BBoxZ1 = bs.readFloat()
   #BBoxX2 = bs.readFloat()
   #BBoxY2 = bs.readFloat()
   #BBoxZ2 = bs.readFloat()
   #BBoxScaleX1 = bs.readFloat()
   #BBoxScaleY1 = bs.readFloat()
   #BBoxScaleZ1 = bs.readFloat()
   #BBoxScaleX2 = bs.readFloat()
   #BBoxScaleY2 = bs.readFloat()
   #BBoxScaleZ2 = bs.readFloat()
   #MipConstantUV0 = bs.readFloat()
   #MipConstantUV1 = bs.readFloat()
   bs.seek(84, NOESEEK_ABS)
   posAli = 0

#MTRL STUFF
   #MatSig = bs.readUInt()
   MatCount = bs.read("L")
   MatNames = []
   pos = bs.tell()
   print(MatCount, pos)
#MTRL LOOP
   for i in range(0, MatCount[0]):
      #MatCharCount = bs.readUInt()
      #print(MatCharCount)
      #MatNames.append (bs.readBytes(MatCharCount).decode("ASCII").rstrip("\0"))
      bs.seek(4, NOESEEK_REL)
      MatNames.append (bs.readString())

#STBS LOOP
   print(MatNames)
   subMeshCount = bs.readUInt()
   print(subMeshCount)
   MatID = []
   VertCount = []
   VertBuffType = []
   FaceCount = []
   FaceType = []
   BoneIDS = []
   BIXD = []
   BoneIDLOC = []
   BoneIDS = []
   
   mdl = []
   VertID = []
   MorphVertPOS = []
   MorphVertNorm = []
   MorphFrameCountID = []
   MDLWritten = rapi.getInputName()
   MDLWrite = NoeBitStream()
   topname = rapi.getExtensionlessName(rapi.getExtensionlessName(rapi.getInputName()))
   for i in range(0, subMeshCount):
      BoneIDSPre = []
      print("Sub Mesh", i)
      tsbsSig = bs.readUInt()
      print(tsbsSig)
      MatID.append (bs.readUInt())
      Blank2 = bs.readUInt()
      BVXD = bs.readUInt()
      VertCount.append (bs.readUInt())
      VertBuffType.append (bs.readUShort())
      print(VertBuffType[i])
      MorphFrameCount = bs.readUInt()
      MorphFrameCountID.append (MorphFrameCount)
      if MorphFrameCount is 0:
         print(MorphFrameCount, "Morph Frame Count is 0")
         
      if MorphFrameCount is not 0:
         print(MorphFrameCount, "Morph Frame Count is not 0")
         n = 0
         MorphVertCountList = []
         FrameLOC = []
         FrameOrder = []
         for m in range(0, MorphFrameCount):
            pos = bs.tell()
            FrameLOC.append (pos)
            MorphVertCount = bs.readUInt()
            MorphVertCountList.append (MorphVertCount)
            #print("MorphVertCount", MorphVertCount)
            #n = 0
            FrameName = ("Frame_" + str(n))
            n = (n + 1)
            Frame = []
            for mv in range(0, MorphVertCount):
               VertID.append(bs.readUInt())
               VertX = bs.readUShort()
               #pos = bs.tell()
               #VertX = (VertX / 32767)
               VertY = bs.readUShort()
               #pos = bs.tell()
               #VertY = (VertY / 32767)
               VertZ = bs.readUShort()
               #pos = bs.tell()
               #VertZ = (VertZ / 32767)
               VertNormX = bs.readUShort()
               VertNormY = bs.readUShort()
               VertNormZ = bs.readUShort()
               bs.seek(8, NOESEEK_REL)
               #pos = bs.tell()
         for mc in range(0, MorphFrameCount):
            FrameOrder.append(bs.readUShort())
         FinalMorphCount = bs.readUShort()
         MorphCharCount = bs.readUInt()
         MorphName = bs.readString()
         print(MorphName)
            
      if VertBuffType[i] == int(768) or VertBuffType[i] == int(256):
         bs.seek(3, NOESEEK_REL)
      pos = bs.tell()
      BIXD.append (pos)
      BIXDSig = bs.readUInt()
      Blank2 = bs.readUInt()
      FaceCount.append (bs.readUInt())
      FaceType.append (bs.readUInt())
      pos = bs.tell()
      BoneIDLOC.append (pos)
      BoneIDCount = bs.readUByte()
      for bi in range(0, BoneIDCount):
         BoneIDSPre.append (bs.readUByte())
      BoneIDS.append(BoneIDSPre)
      bs.seek(56, NOESEEK_REL)
      if VertBuffType[i] == (1280,):
         crap = bs.readUShort()
         VertBuffType[i] = (1024,)
   print("MaterialIDS", MatID)
#RigStuff
   if VertBuffType[0] == int(1024) or VertBuffType[0] == int(768):
      boneReList = RigStuff(VertBuffType, topname)
      
#MDLSourceStuff
   MeshExists = rapi.checkFileExists(topname+str(".Mesh"))
   if MeshExists:
      MDLFile = rapi.loadIntoByteArray(topname+str(".Mesh"))
   else:
      MDLFile = rapi.loadPairedFile("Brutal Legend", ".Mesh")
   MDL = NoeBitStream(MDLFile)
   MeshStarts = []
   MeshFaceStarts = []
   BONINDBUFF = []

   #print("MeshStarts", MeshStarts, "MeshFaceStarts", MeshFaceStarts)
   print("MDL AT ",MDL.tell())
   for s in range(0, subMeshCount):
      Face = []

      POS, NORM, TAN, UV1, UV2, COL1, COL2, BI, BW = VertStuff(MDL, VertCount[s], VertBuffType[s])
      POS = struct.pack('B'*len(POS), *POS)
      NORM = struct.pack('B'*len(NORM), *NORM)
      TAN = struct.pack('B'*len(TAN), *TAN)
      UV1 = struct.pack('B'*len(UV1), *UV1)
      UV2 = struct.pack('B'*len(UV2), *UV2)
      if VertBuffType[s] == int(1024) or VertBuffType[s] == int(512):
         rapi.rpgBindPositionBuffer(POS, noesis.RPGEODATA_HALFFLOAT, 8)
         rapi.rpgBindNormalBuffer(NORM, noesis.RPGEODATA_HALFFLOAT, 8)
         rapi.rpgBindTangentBuffer(TAN, noesis.RPGEODATA_HALFFLOAT, 8)
         rapi.rpgBindUV1Buffer(UV1, noesis.RPGEODATA_HALFFLOAT, 4)
         rapi.rpgBindUV2Buffer(UV2, noesis.RPGEODATA_HALFFLOAT, 4)
      if VertBuffType[s] == int(768) or VertBuffType[s] == int(256):
         rapi.rpgBindPositionBuffer(POS, noesis.RPGEODATA_FLOAT, 12)
         rapi.rpgBindNormalBuffer(NORM, noesis.RPGEODATA_FLOAT, 12)
         #rapi.rpgBindTangentBuffer(TAN, noesis.RPGEODATA_FLOAT, 16)
         rapi.rpgBindUV1Buffer(UV1, noesis.RPGEODATA_FLOAT, 8)
         rapi.rpgBindUV2Buffer(UV2, noesis.RPGEODATA_FLOAT, 8)
      if VertexBool:
         COL = COL2
      else:
         COL = COL1
      COL = struct.pack('B'*len(COL), *COL)
      #VertColor = BGRA            
      rapi.rpgBindColorBuffer(COL, noesis.RPGEODATA_UBYTE, 4, 4)
      if VertBuffType[s] == int(1024) or VertBuffType[s] == int(768):
         rapi.rpgSetBoneMap(BoneIDS[s])
         IDS = struct.pack('B'*len(BI), *BI)
         WEIGHTS = struct.pack('B'*len(BW), *BW)
         if ExportSkin:
            print("Bind Skin")
            rapi.rpgBindBoneIndexBuffer(IDS, noesis.RPGEODATA_BYTE, 4, 4)
            rapi.rpgBindBoneWeightBuffer(WEIGHTS, noesis.RPGEODATA_UBYTE, 4, 4)
      FaceBuff = MDL.readBytes(FaceCount[s] * 2)
      # FaceBuff = struct.pack('H'*len(Face), *Face)
      if MorphFrameCountID[s] is not 0:
##            RETURN = bs.tell()
         for mf in range(0, MorphFrameCountID[s]):
      
            bs.seek(FrameLOC[mf], NOESEEK_ABS)
            # print(FrameLOC[mf], FlexNames[FrameOrder[mf]])
            MorphVertCount = bs.readUInt()
            FramePOS = []
            FrameNorm = []
            FrameTan = []
            FrameIDS = []
            MorphPOS = []
            MorphNorm = []
            MorphTan = []
            for mm in range(0,MorphVertCount):
               FrameIDS.append(bs.readUInt())
               MPOSX = (((bs.readShort() / 32767) * 2))
               MPOSY = (((bs.readShort() / 32767) * 2))
               MPOSZ = (((bs.readShort() / 32767) * 2))
               MNORMX = (((bs.readShort() / 32767) * 2))
               MNORMY = (((bs.readShort() / 32767) * 2))
               MNORMZ = (((bs.readShort() / 32767) * 2))
               MTANX = (((bs.readShort() / 32767) * 2))
               MTANY = (((bs.readShort() / 32767) * 2))
               MTANZ = (((bs.readShort() / 32767) * 2))
               MTANW = (((bs.readShort() / 32767) * 2))
               FramePOS.append((float(MPOSX), float(MPOSY), float(MPOSZ)))
               FrameNorm.append((float(MNORMX), float(MNORMY), float(MNORMZ)))
               FrameTan.append((float(MTANX), float(MTANY), float(MTANZ), float(MTANW)))
            for mv in range(0,VertCount[s]):
               if mv in FrameIDS:
                  ID = FrameIDS.index(mv)
                  MorphPOS.append(FramePOS[ID])
                  MorphNorm.append(FrameNorm[ID])
                  MorphTan.append(FrameTan[ID])
               else:
                  MorphPOS.append((float(0.0), float(0.0), float(0.0)))
                  MorphNorm.append((float(0.0), float(0.0), float(0.0)))
                  MorphTan.append((float(0.0), float(0.0), float(0.0), float(0.0)))
            MPOSBUFF3 = list(itertools.chain.from_iterable(MorphPOS))
            MNORMBUFF = list(itertools.chain.from_iterable(MorphNorm))
            MTANBUFF = list(itertools.chain.from_iterable(MorphTan))
            #rapi.rpgSetName(MeshName)
            MPOS = struct.pack('f'*len(MPOSBUFF3), *MPOSBUFF3)
            MNORM = struct.pack('f'*len(MNORMBUFF), *MNORMBUFF)
            MTAN = struct.pack('f'*len(MTANBUFF), *MTANBUFF)
            rapi.rpgFeedMorphTargetPositions(MPOS, noesis.RPGEODATA_FLOAT, 12)
            rapi.rpgFeedMorphTargetNormals(MNORM, noesis.RPGEODATA_FLOAT, 12)
            rapi.rpgCommitMorphFrame(VertCount[s])
            MPOSBUFF = []
            MNORMBUFF = []
            MTANBUFF = []
            MPOS = None
            MNORM = None
            MTAN = None
         rapi.rpgCommitMorphFrameSet()
      Mesh = ("Mesh_" + str(s))
      MeshName = str(Mesh)
      rapi.rpgSetName(MeshName)
      print(MatNames[MatID[s]])
      CurrentMaterial = MatNames[MatID[s]]
      CurrentMaterial = CurrentMaterial.replace('/', '_')
      rapi.rpgSetMaterial(CurrentMaterial)
      rapi.rpgSmoothTangents()
      if FaceType[s] == 2:
         rapi.rpgCommitTriangles(FaceBuff, noesis.RPGEODATA_USHORT, FaceCount[s], noesis.RPGEO_TRIANGLE, 1)
      else:
         rapi.rpgCommitTriangles(FaceBuff, noesis.RPGEODATA_USHORT, FaceCount[s], noesis.RPGEO_TRIANGLE_STRIP, 1)
      rapi.rpgClearBufferBinds()

   mdl = rapi.rpgConstructModel()
   
   if LOADANIM == (0):
      print("No Anim")
      if VertBuffType[0] == int(1024) or VertBuffType[0] == int(768):
         mdl.setBones(boneReList)
      mdlList.append(mdl) #important, don't forget to put your loaded model in the mdlList
    
      
   return 1





