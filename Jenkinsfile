def buildVersion
def boards_to_build = ["WiPy", "LoPy", "SiPy", "GPy", "FiPy", "LoPy4"]
def boards_to_test = ["FiPy_868":"FIPY_868", "LoPy_868":"LOPY_868"]
String remote_node = "UDOO"

node {
    // get pycom-esp-idf source
    stage('Checkout') {
        checkout scm
        sh 'rm -rf esp-idf'
        sh 'git clone --depth=1 --recursive -b master https://github.com/pycom/pycom-esp-idf.git esp-idf'
    }

    stage('mpy-cross') {
        // build the cross compiler first
        sh '''export GIT_TAG=$(git rev-parse --short HEAD)
          git tag -fa v1.8.6-849-$GIT_TAG -m \\"v1.8.6-849-$GIT_TAG\\";
          cd mpy-cross;
          make clean;
          make all'''
    }

    stage('IDF-LIBS') {
        // build the libs from esp-idf
       sh '''export PATH=$PATH:/opt/xtensa-esp32-elf/bin;
        		 export IDF_PATH=${WORKSPACE}/esp-idf;
        		 cd $IDF_PATH/examples/wifi/scan;
        		 make clean && make all'''
    }

 	for (board in boards_to_build) {
		stage(board) {
			def parallelSteps = [:]
            def board_u = board.toUpperCase()
            if (board_u == "LOPY" || board_u == "FIPY"  || board_u == "LOPY4") {
        			parallelSteps[board+"_868"] = boardBuild(board+"_868")
        			parallelSteps[board+"_915"] = boardBuild(board+"_915")
        		}
    			else{
        			parallelSteps[board] = boardBuild(board)
        		}
  		}
  	}

    stash includes: '**/*.bin', name: 'binary'
    stash includes: 'tests/**', name: 'tests'
    stash includes: 'esp-idf/components/esptool_py/**', name: 'esp-idfTools'
    stash includes: 'tools/**', name: 'tools'
    stash includes: 'esp32/tools/**', name: 'esp32Tools'
}

    stage ('Flash') {
      def parallelFlash = [:]
      for (x in boards_to_test) {
        def name = x.toUpperCase()
        parallelFlash[name] = flashBuild(name,x.value)
      }
    parallel parallelFlash
    }

    stage ('Test'){
      def parallelTests = [:]
      for (board_name in boards_to_test) {
        parallelTests[board_name] = testBuild(board_name.toUpperCase(),board_name.value)
      }
    parallel parallelTests
    }

    def testBuild(name, device) {
      return {
        node(remote_node) {
          sleep(5) //Delay to skip all bootlog
          dir('tests') {
            timeout(30) {
              sh '''./run-tests --target=esp32-''' + name + ''' --device /dev/''' + device
            }
          }
          sh 'python esp32/tools/pypic.py --port /dev/' + device +' --enter'
          sh 'python esp32/tools/pypic.py --port /dev/' + device +' --exit'
        }
      }
    }

def flashBuild(name,device) {
  return {
    node(remote_node) {
      sh 'rm -rf *'
      unstash 'binary'
      unstash 'esp-idfTools'
      unstash 'esp32Tools'
      unstash 'tests'
      unstash 'tools'
      sh 'python esp32/tools/pypic.py --port /dev/' + device +' --enter'
      sh 'esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 --port /dev/' + device +' --baud 921600 erase_flash'
      sh 'python esp32/tools/pypic.py --port /dev/' + device +' --enter'
      sh 'esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 --port /dev/' + device +' --baud 921600 --before no_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0x1000 esp32/build/'+ name +'/release/bootloader/bootloader.bin 0x8000 esp32/build/'+ name +'/release/lib/partitions.bin 0x10000 esp32/build/'+ name +'/release/appimg.bin'
      sh 'python esp32/tools/pypic.py --port /dev/' + device +' --exit'
    }
  }
}

def boardBuild(name) {
    def name_u = name.toUpperCase()
    def name_short = name_u.split('_')[0]
    def lora_band = ""
    if (name_u == "LOPY_868" || name_u == "FIPY_868"  || name_u == "LOPY4_868") {
        lora_band = " LORA_BAND=USE_BAND_868"
    }
    else if (name_u == "LOPY_915" || name_u == "FIPY_915" || name_u == "LOPY4_915") {
        lora_band = " LORA_BAND=USE_BAND_915"
    }
    def app_bin = name.toLowerCase() + '.bin'
    return {
    		release_dir = "${JENKINS_HOME}/release/${JOB_NAME}"
        sh '''export PATH=$PATH:/opt/xtensa-esp32-elf/bin;
        export IDF_PATH=${WORKSPACE}/esp-idf;
        cd esp32;
        make clean BOARD=''' + name_short + lora_band

        sh '''export PATH=$PATH:/opt/xtensa-esp32-elf/bin;
        export IDF_PATH=${WORKSPACE}/esp-idf;
        cd esp32;
        make TARGET=boot -j2 BOARD=''' + name_short + lora_band

        sh '''export PATH=$PATH:/opt/xtensa-esp32-elf/bin;
        export IDF_PATH=${WORKSPACE}/esp-idf;
        cd esp32;
        make TARGET=app -j2 BOARD=''' + name_short + lora_band

        sh '''cd esp32/build/'''+ name_u +'''/release;
        export PYCOM_VERSION=$(cat ../../../pycom_version.h |grep SW_VERSION_NUMBER|cut -d\\" -f2);
        export GIT_TAG=$(git rev-parse --short HEAD);
        mkdir -p firmware_package;
        mkdir -p '''+ release_dir + '''/\$PYCOM_VERSION/\$GIT_TAG;
        cd firmware_package;
        cp ../bootloader/bootloader.bin .;
        mv ../application.elf ''' + release_dir + '''/\$PYCOM_VERSION/\$GIT_TAG/''' + name + '''-\$PYCOM_VERSION-application.elf;
        cp ../appimg.bin .;
        cp ../lib/partitions.bin .;
        cp ../../../../boards/''' + name_short + '''/''' + name_u + '''/script .;
        cp ../''' + app_bin + ''' .;'''
        if (${BRANCH_NAME} == "master") {
          sh '''tar -cvzf ''' + release_dir + '''/\$PYCOM_VERSION/\$GIT_TAG/''' + name + '''-\$PYCOM_VERSION.tar.gz  appimg.bin  bootloader.bin   partitions.bin   script ''' + app_bin
        }
    }
}

def version() {
    def matcher = readFile('esp32/build/LOPY/release/genhdr/mpversion.h') =~ 'MICROPY_GIT_TAG (.+)'
    matcher ? matcher[0][1] : null
}
