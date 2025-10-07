package com.example.archeonetwebviewdemo // <-- Change this to match your actual package if needed

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.webkit.*
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceError
import android.webkit.SslErrorHandler
import android.net.http.SslError


class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var urlInput: EditText
    private val LOCATION_PERM_CODE = 123

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        urlInput = findViewById(R.id.urlInput)
        val loadBtn: Button = findViewById(R.id.loadBtn)
        webView = findViewById(R.id.webview)

        checkLocationPermissions()
        setupWebView()

        // Set default URL—change this to your Streamlit server if needed
        urlInput.setText("https://192.168.1.100:8501")
        loadBtn.setOnClickListener {
            val url = urlInput.text.toString().trim()
            if (url.isNotEmpty()) webView.loadUrl(url)
        }

        // Auto-load at startup
        webView.loadUrl(urlInput.text.toString())
    }

    private fun setupWebView() {
        webView.setBackgroundColor(0xFFFFFFFF.toInt()) // Ensure WebView background is always white

        val s = webView.settings
        s.javaScriptEnabled = true
        s.domStorageEnabled = true
        s.allowFileAccess = true
        s.javaScriptCanOpenWindowsAutomatically = true
        s.mediaPlaybackRequiresUserGesture = false
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) s.safeBrowsingEnabled = false
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            s.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        // Make links stay inside the WebView, handle SSL errors for self-signed certs
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                return false
            }

            override fun onReceivedSslError(
                view: WebView?,
                handler: SslErrorHandler?,
                error: SslError?
            ) {
                handler?.proceed() // Accept ALL SSL certs for dev
            }


            override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
                Toast.makeText(this@MainActivity, "Web error: ${error.description}", Toast.LENGTH_LONG).show()
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onGeolocationPermissionsShowPrompt(origin: String?, callback: GeolocationPermissions.Callback?) {
                callback?.invoke(origin, true, true) // Always allow geolocation
            }
        }
    }

    private fun checkLocationPermissions() {
        val need = mutableListOf<String>()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            need += Manifest.permission.ACCESS_FINE_LOCATION
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            need += Manifest.permission.ACCESS_COARSE_LOCATION
        if (need.isNotEmpty())
            ActivityCompat.requestPermissions(this, need.toTypedArray(), LOCATION_PERM_CODE)
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) webView.goBack()
        else super.onBackPressed()
    }
}
