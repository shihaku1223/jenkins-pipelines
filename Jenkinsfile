import java.text.SimpleDateFormat
import java.io.File;
import java.io.FilenameFilter;

def getLastSuccessBuild(build)
{
    if(build == null)
        return null
    
    prev = build.getPreviousBuild()
    
    if(prev == null)
        return null

    if(prev.result == 'SUCCESS')
        return prev
    return getLastSuccessBuild(prev)
}

def getBuildTime(build) {
    
    if(build == null)
        return '19871223000000'
    date = new Date(build.getTimeInMillis())
    dateFormat = new SimpleDateFormat("yyyyMMddHHmmss");

    return dateFormat.format(date)
}

def getFiles(String baseDir, String endsWith) {
    File dir = new File(baseDir)
    return Arrays.asList(dir.listFiles( new FilenameFilter() {
      public boolean accept(File d, String name) {
        if(filename == null)
            return true;

        if (name.endsWith(endsWith))
            return true;
        return false;
      }
    }
    ))
}

pipeline {
  agent { node { label 'linux-docker-slave' } }
  stages {
    stage('checkout')  {
      steps {
        cleanWs()
        checkout([$class: 'SubversionSCM', additionalCredentials: [], excludedCommitMessages: '', excludedRegions: '', excludedRevprop: '', excludedUsers: '', filterChangelog: false, ignoreDirPropChanges: false, includedRegions: '', locations: [[cancelProcessOnExternalsFail: true, credentialsId: '3fc54269-d115-4e30-983c-55616a93c22f', depthOption: 'infinity', ignoreExternalsOption: true, local: '.', remote: 'http://osoft-de-c.olympus.co.jp/svn/ipf3/offshore-src/tools/DebugLog/cvapp-log-analyzer'], [cancelProcessOnExternalsFail: true, credentialsId: '3fc54269-d115-4e30-983c-55616a93c22f', depthOption: 'infinity', ignoreExternalsOption: true, local: 'mantis_utils', remote: 'http://osoft-de-c.olympus.co.jp/svn/ipf3/offshore-src/tools/utility/mantis_utils'], [cancelProcessOnExternalsFail: true, credentialsId: '3fc54269-d115-4e30-983c-55616a93c22f', depthOption: 'infinity', ignoreExternalsOption: true, local: 'debug-symbol', remote: 'http://osoft-de-c.olympus.co.jp/svn/ipf3/offshore-src/tools/DebugLog/DebugLogFormatter']], quietOperation: true, workspaceUpdater: [$class: 'UpdateUpdater']])
      }
    }
    stage('get-last-build-time') {
      steps {
        script  {

          build = getLastSuccessBuild(currentBuild)
          
          LAST_BUILD_TIME = getBuildTime(build)
          println('last cussess build time:' + LAST_BUILD_TIME)
        }
      }
    }
    stage('prepare') {
      environment {
          http_proxy = 'http://proxy.olympus.co.jp:8080'
          https_proxy = 'http://proxy.olympus.co.jp:8080'
      }
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('parse') {
      environment {
          LAST_BUILD_TIME = "${LAST_BUILD_TIME}"
          http_proxy = 'http://proxy.olympus.co.jp:8080'
          https_proxy = 'http://proxy.olympus.co.jp:8080'
      }
      steps {
        withCredentials([usernamePassword(credentialsId: '3fc54269-d115-4e30-983c-55616a93c22f', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
          script  {
            try {
              STATUS = sh(returnStatus: true,
                script: '''
                  python3 ./analyzer.py -z -a -t debug-symbol/logFormatSymbolsCv2k.csv \
                  -P 'CV2KApp窓口' \
                  --url 'http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl' \
                  --username $USERNAME --password $PASSWORD -f $LAST_BUILD_TIME
                  ''')
            } catch(Exception ex) {
                println(ex)
                currentBuild.result = 'FAILURE'
                error(ex)
            }
          }
        }
      }
    }
    stage('list-archive')  {
      environment {
          http_proxy = 'http://proxy.olympus.co.jp:8080'
          https_proxy = 'http://proxy.olympus.co.jp:8080'
      }
      steps {
        script  {
          files = findFiles(glob: '*.tar.bz2')
          for(file in files) {
            echo """
             ${file.name} ${file.path} ${file.directory} ${file.length} ${file.lastModified}
            """
            withCredentials([usernamePassword(credentialsId: '3fc54269-d115-4e30-983c-55616a93c22f', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
              name = file.path
              issueId = name.substring(0, name.indexOf('.'))
              println('add note to issud:' + issueId)
              sh """
                python3 ./analyzer.py -t debug-symbol/logFormatSymbolsCv2k.csv \
                  -P 'CV2KApp窓口' \
                  --url 'http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl' \
                  --username $USERNAME --password $PASSWORD \
                  --issueId $issueId \
                  --message "ログ解析結果\n\\\\\\\\osw-de-01.is.olympus.global\\f3share\\ci_data\\app_service_desk\\log_analysis\\build-$BUILD_NUMBER\\${file.path}"
               """
            }
          }
        }
      }
    }
  
    stage('publish')  {
      steps {
        script  {
          println('number of parsed log: ' + STATUS)
          cifsPublisher(publishers: [[configName: 'f3user-log_analysis', transfers: [[cleanRemote: false, excludes: '', flatten: true, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: ',', remoteDirectory: 'build-$BUILD_NUMBER', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '*.tar.bz2']], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: true]])
        }
      }
    }
  }
}
