<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.10.2" name="cave_crawler_v2" tilewidth="16" tileheight="16" spacing="1" tilecount="225" columns="15">
 <image source="../gfx/cave_crawler_v2.png" width="256" height="256"/>
 <tile id="45">
  <properties>
   <property name="kills you" type="bool" value="true"/>
   <property name="light" type="float" value="30"/>
  </properties>
  <animation>
   <frame tileid="45" duration="300"/>
   <frame tileid="46" duration="300"/>
   <frame tileid="47" duration="300"/>
  </animation>
 </tile>
 <tile id="46">
  <properties>
   <property name="kills you" type="bool" value="true"/>
   <property name="light" type="float" value="30"/>
  </properties>
 </tile>
 <tile id="47">
  <properties>
   <property name="kills you" type="bool" value="true"/>
   <property name="light" type="float" value="30"/>
  </properties>
 </tile>
 <tile id="48">
  <properties>
   <property name="light" type="float" value="50"/>
  </properties>
  <animation>
   <frame tileid="48" duration="1000"/>
   <frame tileid="63" duration="1000"/>
  </animation>
 </tile>
 <tile id="49">
  <properties>
   <property name="light" type="float" value="50"/>
  </properties>
 </tile>
 <tile id="50">
  <properties>
   <property name="light" type="float" value="50"/>
  </properties>
 </tile>
 <tile id="51">
  <properties>
   <property name="light" type="float" value="50"/>
  </properties>
 </tile>
 <tile id="63">
  <properties>
   <property name="light" type="float" value="50"/>
  </properties>
 </tile>
 <tile id="66">
  <properties>
   <property name="water" type="bool" value="true"/>
  </properties>
 </tile>
 <tile id="94">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="95">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="96">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="109">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="110">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
 <tile id="111">
  <properties>
   <property name="passable" type="bool" value="false"/>
  </properties>
 </tile>
</tileset>
