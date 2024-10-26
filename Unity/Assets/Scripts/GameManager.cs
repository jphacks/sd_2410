using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    [SerializeField] AvaterManager _avaterManager;
    AudioClip _audioClip;
    FileSystemWatcher fileWatcher;
    private ConcurrentQueue<string> audioFileQueue = new ConcurrentQueue<string>();

    void Start()
    {
        fileWatcher = new FileSystemWatcher(Application.dataPath + "/Audio");

        // FileSystemWatcher�̐ݒ�
        fileWatcher.NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName;
        fileWatcher.Filter = "*.wav"; // �Ď��Ώۃt�@�C���̃t�B���^�i��F.txt�t�@�C���̂݁j

        // �C�x���g�n���h���̓o�^
        fileWatcher.Changed += OnFileChanged;
        fileWatcher.Created += OnFileChanged;
        fileWatcher.Renamed += OnFileChanged;

        // �Ď����J�n
        fileWatcher.EnableRaisingEvents = true;
    }

    // �t�@�C�����ύX���ꂽ�Ƃ��Ɏ��s�����֐�

    //private void OnFileChanged(object sender, FileSystemEventArgs e)
    //{
    //    Debug.Log($"File {e.ChangeType}: {e.FullPath}");

    //    //System.Threading.Thread.Sleep(100);

    //    Debug.Log(e.FullPath);
    //    // �����œ���̏��������s
    //    StartCoroutine(LoadAudioClip(e.FullPath));
    //}

    private void OnFileChanged(object sender, FileSystemEventArgs e)
    {
        // �t�@�C���p�X���L���[�ɒǉ�
        audioFileQueue.Enqueue(e.FullPath);
    }

    void Update()
    {
        // �L���[�Ƀt�@�C���p�X������Ύ擾���ď���
        if (audioFileQueue.TryDequeue(out string filePath))
        {
            StartCoroutine(LoadAudioClip(filePath));
        }
    }

    private IEnumerator LoadAudioClip(string filePath)
    {
        string url = "file:///" + filePath;

        using (WWW www = new WWW(url))
        {
            yield return www;
            _audioClip = www.GetAudioClip(true, true);

            // �A�j���[�V�����Đ�
            _avaterManager.GetAudioText(_audioClip);

            Debug.Log("New audio file played: " + filePath);
        }
    }

    void OnDestroy()
    {
        // �Ď����~
        fileWatcher.EnableRaisingEvents = false;
        fileWatcher.Dispose();
        Debug.Log("File watcher stopped.");
    }
}