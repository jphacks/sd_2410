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

        // FileSystemWatcherの設定
        fileWatcher.NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName;
        fileWatcher.Filter = "*.wav"; // 監視対象ファイルのフィルタ（例：.txtファイルのみ）

        // イベントハンドラの登録
        fileWatcher.Changed += OnFileChanged;
        fileWatcher.Created += OnFileChanged;
        fileWatcher.Renamed += OnFileChanged;

        // 監視を開始
        fileWatcher.EnableRaisingEvents = true;
    }

    // ファイルが変更されたときに実行される関数

    //private void OnFileChanged(object sender, FileSystemEventArgs e)
    //{
    //    Debug.Log($"File {e.ChangeType}: {e.FullPath}");

    //    //System.Threading.Thread.Sleep(100);

    //    Debug.Log(e.FullPath);
    //    // ここで特定の処理を実行
    //    StartCoroutine(LoadAudioClip(e.FullPath));
    //}

    private void OnFileChanged(object sender, FileSystemEventArgs e)
    {
        // ファイルパスをキューに追加
        audioFileQueue.Enqueue(e.FullPath);
    }

    void Update()
    {
        // キューにファイルパスがあれば取得して処理
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

            // アニメーション再生
            _avaterManager.GetAudioText(_audioClip);

            Debug.Log("New audio file played: " + filePath);
        }
    }

    void OnDestroy()
    {
        // 監視を停止
        fileWatcher.EnableRaisingEvents = false;
        fileWatcher.Dispose();
        Debug.Log("File watcher stopped.");
    }
}